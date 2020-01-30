from contextlib import ExitStack
from copy import deepcopy

from django.test import SimpleTestCase

import attr
from mock import patch
from testil import Config

from corehq.form_processor.parsers.ledgers.helpers import UniqueLedgerReference

from .. import casediff as mod
from ..statedb import StateDB


class TestDiffCases(SimpleTestCase):

    def setUp(self):
        super(TestDiffCases, self).setUp()
        self.patches = [
            patch(
                "corehq.form_processor.backends.sql.dbaccessors.CaseAccessorSQL.get_cases",
                self.get_sql_cases,
            ),
            patch(
                "corehq.form_processor.backends.sql.dbaccessors"
                ".LedgerAccessorSQL.get_ledger_values_for_cases",
                self.get_sql_ledgers,
            ),
            patch(
                "corehq.apps.commtrack.models.StockState.objects.filter",
                self.get_stock_states,
            ),
            patch(
                "corehq.form_processor.backends.couch.processor"
                ".FormProcessorCouch.hard_rebuild_case",
                self.hard_rebuild_case,
            ),
            patch.object(
                mod.StockTransactionLoader,
                "dedup_stock_state",
                lambda *a: None,
            ),
        ]

        for patcher in self.patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.statedb = StateDB.init("test", ":memory:")
        self.addCleanup(self.statedb.close)
        self.sql_cases = {}
        self.sql_ledgers = {}
        self.couch_cases = {}
        self.couch_ledgers = {}
        stack = ExitStack()
        stack.enter_context(mod.global_diff_state("test", {}))
        self.addCleanup(stack.close)

    def test_clean(self):
        self.add_case("a")
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs()

    def test_diff(self):
        couch_json = self.add_case("a", prop=1)
        couch_json["prop"] = 2
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs([Diff("a", path=["prop"], old=2, new=1)])

    def test_wrong_domain(self):
        couch_json = self.add_case("a", prop=1, domain="wrong")
        couch_json["prop"] = 2
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs([Diff("a", path=["domain"], old="wrong", new="test")])

    def test_replace_diff(self):
        self.add_case("a", prop=1)
        different_cases = deepcopy(self.couch_cases)
        different_cases["a"]["prop"] = 2
        mod.diff_cases_and_save_state(different_cases, self.statedb)
        self.assert_diffs([Diff("a", path=["prop"], old=2, new=1)])
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs()

    def test_replace_ledger_diff(self):
        self.add_case("a")
        stock = self.add_ledger("a", x=1)
        stock.values["x"] = 2
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs([Diff("a/stock/a", "stock state", path=["x"], old=2, new=1)])
        stock.values["x"] = 1
        mod.diff_cases_and_save_state(self.couch_cases, self.statedb)
        self.assert_diffs()

    def assert_diffs(self, expected=None):
        actual = [
            Diff(diff.doc_id, diff.kind, *diff.json_diff)
            for diff in self.statedb.get_diffs()
        ]
        self.assertEqual(actual, expected or [])

    def add_case(self, case_id, **props):
        assert case_id not in self.sql_cases, self.sql_cases[case_id]
        assert case_id not in self.couch_cases, self.couch_cases[case_id]
        props.setdefault("domain", self.statedb.domain)
        props.setdefault("doc_type", "CommCareCase")
        props.setdefault("_id", case_id)
        self.sql_cases[case_id] = Config(
            case_id=case_id,
            props=props,
            to_json=lambda: dict(props, case_id=case_id),
            is_deleted=False,
        )
        self.couch_cases[case_id] = couch_case = dict(props, case_id=case_id)
        return couch_case

    def add_ledger(self, case_id, **values):
        ref = UniqueLedgerReference(case_id, "stock", case_id)
        self.sql_ledgers[case_id] = Config(
            ledger_reference=ref,
            values=values,
            to_json=lambda: dict(values, ledger_reference=ref.as_id()),
        )
        couch_values = dict(values)
        stock = Config(
            ledger_reference=ref,
            values=couch_values,
            to_json=lambda: dict(couch_values, ledger_reference=ref.as_id()),
        )
        self.couch_ledgers[case_id] = stock
        return stock

    def get_sql_cases(self, case_ids):
        return [self.sql_cases[c] for c in case_ids]

    def get_sql_ledgers(self, case_ids):
        ledgers = self.sql_ledgers
        return [ledgers[c] for c in case_ids if c in ledgers]

    def get_stock_states(self, case_id__in):
        ledgers = self.couch_ledgers
        return [ledgers[c] for c in case_id__in if c in ledgers]

    def hard_rebuild_case(self, *args, **kw):
        raise Exception("rebuild disabled")


@attr.s
class Diff:
    doc_id = attr.ib()
    kind = attr.ib(default="CommCareCase")
    type = attr.ib(default="diff")
    path = attr.ib(factory=list)
    old = attr.ib(default=None)
    new = attr.ib(default=None)
