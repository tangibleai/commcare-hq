"""Utilities for assessing and repairing CouchDB corruption"""
import logging
from collections import defaultdict
from itertools import chain
from urllib.parse import urljoin, urlparse, urlunparse

import attr
from couchdbkit import Database
from django.conf import settings

from auditcare.models import AuditEvent
from casexml.apps.case.models import CommCareCase
from corehq.apps.app_manager.models import Application
from corehq.apps.domain.models import Domain
from corehq.apps.users.models import CommCareUser
from corehq.util.couch_helpers import NoSkipArgsProvider
from corehq.util.pagination import ResumableFunctionIterator
from couchforms.models import XFormInstance
from dimagi.utils.parsing import json_format_datetime

log = logging.getLogger(__name__)
DOC_TYPES_BY_NAME = {
    "forms": {
        "type": XFormInstance,
        "date_range": True,
        "use_domain": True,
        "doc_types": [
            'XFormInstance',
            'XFormArchived',
            'XFormDeprecated',
            'XFormDuplicate',
            'XFormError',
            'SubmissionErrorLog',
            'XFormInstance-Deleted',
            'HQSubmission',
        ],
    },
    "cases": {
        "type": CommCareCase,
        "use_domain": True,
        "doc_types": [
            "CommCareCase",
            "CommCareCase-Deleted",
        ],
    },
    "main": {
        "type": XFormInstance,
        "exclude_types": ["forms", "cases"],
    },
    "users": {
        "type": CommCareUser,
        "use_domain": True,
        "date_range": True,  # TODO will this work?
        "doc_types": [
            "CommCareUser",
            "WebUser",
        ],
    },
    "groups": {
        "type": CommCareUser,
        "use_domain": True,
        "exclude_types": ["users"],
    },
    "domains": {"type": Domain},
    "apps": {
        "type": Application,
        "use_domain": True,
    },
    "auditcare": {
        "type": AuditEvent,
        "use_domain": True,
        "view": "auditcare/all_events",
    },
    # TODO
    #"fixtures": {"type": ...},
    #"m4change": {"type": ...},
    #"receiver_wrapper": {"type": ...},
    #"meta": {"type": ...},  # probably don't need to do this one
}


def count_missing_ids(*args):
    def log_result(rec):
        for node, missing in rec.missing.items():
            log.info(f"  {rec.doc_type}, {node}: {len(missing)}")

    rec = None
    results = defaultdict(Result)
    for doc_type, missing_by_db in iter_missing_ids(*args):
        if rec and doc_type != rec.doc_type:
            log_result(rec)
            results.pop(doc_type, None)
        rec = results[doc_type]
        rec.doc_type = doc_type
        for db, new_missing in missing_by_db.items():
            missing = rec.missing.get(db.server.uri, set())
            rec.missing[db.server.uri] = missing | new_missing
    if rec:
        log_result(rec)
    else:
        log.info("no documents found")


@attr.s
class Result:
    doc_type = attr.ib(default=None)
    missing = attr.ib(factory=dict)


def iter_missing_ids(domain, doc_name="ALL", date_range=None, couch_port=15984):
    if doc_name == "ALL":
        groups = DOC_TYPES_BY_NAME
    else:
        groups = {doc_name: DOC_TYPES_BY_NAME[doc_name]}
    for name, group in groups.items():
        log.info("processing %s", name)
        db = group["type"].get_db()
        dates = date_range if group.get("date_range") else None
        domain_name = domain if group.get("use_domain") else None
        view = group.get("view")
        for doc_type in get_doc_types(group):
            itr = _iter_missing_ids(db, doc_type, domain_name, dates, view, couch_port)
            try:
                for rec in itr:
                    yield doc_type, rec["missing"]
            finally:
                itr.discard_state()


#def fix_missing_doc(doc_type, doc_id):
#    ...


def get_doc_types(group):
    if "exclude_types" in group:
        assert "doc_types" not in group, group
        excludes = set(chain.from_iterable(
            DOC_TYPES_BY_NAME[n]["doc_types"] for n in group["exclude_types"]
        ))
        db = group["type"].get_db()
        results = db.view("all_docs/by_doc_type", group_level=1)
        return [r["key"][0] for r in results if r["key"][0] not in excludes]
    return group.get("doc_types", [None])


def _get_couch_node_databases(db, node_port):
    resp = db.server._request_session.get(urljoin(db.server.uri, '/_membership'))
    resp.raise_for_status()
    membership = resp.json()
    nodes = [node.split("@")[1] for node in membership["cluster_nodes"]]

    parsed_url = urlparse(settings.COUCH_DATABASE)._replace(path=f"/{db.dbname}")
    auth = parsed_url.netloc.split('@')[0]

    return [
        Database(urlunparse(parsed_url._replace(netloc=f'{auth}@{node}:{node_port}')))
        for node in nodes
    ]


def _iter_missing_ids(db, doc_type, domain, date_range, view, couch_port, chunk_size=1000):
    databases = _get_couch_node_databases(db, couch_port)

    def data_function(**view_kwargs):
        def get_doc_ids(database=db):
            results = list(database.view(view_name, **view_kwargs))
            if results:
                last_results.append(results[-1])
            return {key(r) for r in results}

        def key(result):
            return tuple(result["key"]) + (result["id"],)

        last_results = []
        missing_results = find_missing_view_results(get_doc_ids, databases)
        if not last_results:
            return []
        last_result = min(last_results, key=key)
        last_result["missing"] = missing_results
        return [last_result]

    if view is not None:
        view_name = view
        start = end = "-"
        startkey = []
        endkey = [{}]
    elif date_range is not None:
        assert domain is not None
        assert doc_type is not None
        view_name = 'by_domain_doc_type_date/view'
        start, end = date_range
        startkey = [domain, doc_type, json_format_datetime(start)]
        endkey = [domain, doc_type, json_format_datetime(end)]
    elif domain is not None and doc_type is not None:
        view_name = 'by_domain_doc_type_date/view'
        start = end = "-"
        startkey = [domain, doc_type]
        endkey = [domain, doc_type, {}]
    elif doc_type is not None:
        view_name = 'all_docs/by_doc_type'
        start = end = "-"
        startkey = [doc_type]
        endkey = [doc_type, {}]
    else:
        view_name = 'all_docs/by_doc_type'
        start = end = "-"
        startkey = []
        endkey = [{}]

    resume_key = f"{db.dbname}.{domain}.{doc_type}.{start}-{end}"
    args_provider = NoSkipArgsProvider({
        'startkey': startkey,
        'endkey': endkey,
        'limit': chunk_size,
        'include_docs': False,
        'reduce': False,
    })

    return ResumableFunctionIterator(resume_key, data_function, args_provider, item_getter=None)

def get_missing_ids(db, doc_type, domain, date_range, couch_port):
    view_name = 'by_domain_doc_type_date/view'
    start, end = date_range
    startkey = [domain, doc_type, json_format_datetime(start)]
    endkey = [domain, doc_type, json_format_datetime(end)]

    def get_view_results(db):
        ret = {
            res["id"]
            for res in db.view(view_name, startkey=startkey, endkey=endkey, include_docs=False, reduce=False)
        }
        l = list(ret)
        print(db.server.uri, len(ret), l[0], l[-1])
        return ret

    databases = _get_couch_node_databases(db, couch_port)
    missing_by = {}
    counts = {}
    last_count = None
    while last_count != counts:
        last_count = {k: len(v) for k, v in missing_by.items()}
        missing_by_db = find_missing_view_results(get_view_results, databases)
        print({k: len(v) for k, v in missing_by_db.items()})
        for db, new_missing in missing_by_db.items():
            missing = missing_by.get(db, set())
            missing_by[db] = missing | new_missing
    counts = {k: len(v) for k, v in missing_by.items()}
    print(last_count)
    print(counts)


def find_missing_view_results(get_view_results, databases):
    """Find view results that are missing on each database"""
    db_results = {db: get_view_results(db) for db in databases}
    missing = {}
    for db, results in db_results.items():
        all_others = set().union(*[
            other_results
            for other_db, other_results in db_results.items()
            if db != other_db
        ])
        missing[db] = all_others - results
    return missing
