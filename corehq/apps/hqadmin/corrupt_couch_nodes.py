import logging
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from couchdbkit import Database

from .corrupt_couch import DOC_TYPES_BY_NAME

log = logging.getLogger(__name__)


def get_dbname(doc_name):
    db = DOC_TYPES_BY_NAME[doc_name]["type"].get_db()
    return db.dbname


def get_node_dbs(nodes, dbname, username="admin"):
    def node_url(proxy_url, node):
        return urlunparse(proxy_url._replace(netloc=f'{auth}@{node}'))

    proxy_url = urlparse(settings.COUCH_DATABASE)._replace(path=f"/{dbname}")
    auth = username + ":" + proxy_url.netloc.split('@')[0].split(":", 1)[1]
    return [Database(node_url(proxy_url, node)) for node in nodes]


def print_missing_ids(*args):
    for doc_id in iter_missing_ids(*args):
        print(doc_id)


def iter_missing_ids(dbs, id_range, chunk_size=10000):
    start_id, end_id = id_range
    db0, *other_dbs = dbs
    next_id = start_id
    end_id = end_id or {}
    drop = False
    while True:
        db0_ids = query_ids(db0, (next_id, end_id), chunk_size)
        last_id = db0_ids[-1] if db0_ids else {}
        id_sets = query_dbs(other_dbs, (next_id, last_id))
        id_sets.append(db0_ids)
        if drop:
            for ids in id_sets:
                ids.discard(next_id)
        else:
            drop = True
        if not any(id_sets):
            log.info(f"final range: {next_id} - {last_id}")
            break
        missing = find_missing(id_sets)
        log.info(f"{next_id} - {last_id} => {len(missing)}")
        yield from missing
        next_id = last_id


def query_ids(db, id_range, limit=None):
    start, end = id_range
    view_kwargs = {
        "startkey": [start],
        "endkey": [end],
        "include_docs": False,
        "reduce": False,
    }
    if limit:
        view_kwargs["limit"] = limit
    return {rec["id"] for rec in db.view("_all_docs", **view_kwargs)}


def query_dbs(dbs, *args, **kw):
    return [query_ids(db, *args, **kw) for db in dbs]


def find_missing(id_sets):
    """Find ids not present in all sets of ids"""
    return set.union(*id_sets) - set.intersection(*id_sets)


def check_node_integrity(dbs, id_range, chunk_size=10000, min_tries=50):
    """Check each db node for consistent results over a given id range"""
    start_id, end_id = id_range
    next_ids = [start_id] * len(dbs)
    end_id = end_id or {}
    while True:
        for i, db in enumerate(dbs):
            uri = db.uri.rsplit("@")[-1]
            next_id = next_ids[i]
            log.info(f"checking {chunk_size} ids on {uri} starting at {next_id}...")
            reference = None
            for x in range(min_tries):
                ids = query_ids(db, (next_id, end_id), chunk_size)
                if not ids or len(ids) == 1:
                    log.info(f"empty set: {next_id} - {end_id}")
                    assert reference is None, sorted(reference)[:10]
                    return
                if reference is None:
                    reference = ids
                    continue
                if ids != reference:
                    log.warning(f"integrity violation: {uri} on {x + 1} tries")
                    log.debug("diff: %s", reference ^ ids)
                    break
            next_ids[i] = max(reference)
