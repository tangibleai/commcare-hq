from collections import namedtuple

from testil import eq

from ..corrupt_couch import find_missing_view_results


def test_find_missing_view_results():
    DB = namedtuple("DB", "uri")

    def test(result_sets, expected):
        assert len(result_sets) == len(expected)

        def get_ids(db):
            return result_sets[db.uri]

        expected = {DB(i): exp for i, exp in enumerate(expected)}
        missing_results = find_missing_view_results(get_ids, list(expected))
        eq(missing_results, expected)

    yield test, [{1, 2}, {1, 2}], [set(), set()]
    yield test, [{1, 2}, {1, 3}, {2, 4}], [{3, 4}, {2, 4}, {1, 3}]
    yield test, [{1, 2}, {2, 3}, {1, 2, 3, 4}], [{3, 4}, {1, 4}, set()]
