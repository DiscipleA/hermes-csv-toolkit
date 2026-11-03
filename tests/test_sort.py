import csv
import io
import unittest

from tests.helpers import run_cli


class SortTests(unittest.TestCase):
    def assert_sort(self, text, column, expected):
        result = run_cli("sort", "--column", column, text=text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(list(csv.reader(io.StringIO(result.stdout))), expected)

    def test_sorts_by_named_column_not_first_column(self):
        self.assert_sort("name,score\nAda,10\nLin,2\nZoe,1\n", "score",
                         [["name", "score"], ["Zoe", "1"], ["Ada", "10"], ["Lin", "2"]])

    def test_preserves_quoted_fields_and_multiline_values(self):
        self.assert_sort('name,note\nZoe,"said ""hi"""\n"Doe, Jane","line1\nline2"\n',
                         "name", [["name", "note"], ["Doe, Jane", "line1\nline2"],
                                  ["Zoe", 'said "hi"']])

    def test_equal_keys_keep_original_order(self):
        self.assert_sort("name,group\nZoe,a\nAda,a\nLin,b\n", "group",
                         [["name", "group"], ["Zoe", "a"], ["Ada", "a"], ["Lin", "b"]])

    def test_header_only_is_valid_and_preserves_header(self):
        self.assert_sort("name,score\n", "score", [["name", "score"]])

    def test_empty_field_is_a_valid_sort_key(self):
        self.assert_sort("name,score\nAda,2\nLin,\n", "score",
                         [["name", "score"], ["Lin", ""], ["Ada", "2"]])
