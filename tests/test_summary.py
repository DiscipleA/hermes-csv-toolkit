import json
import unittest

from tests.helpers import run_cli


class SummaryTests(unittest.TestCase):
    def assert_summary(self, text, columns, row_count):
        result = run_cli("summary", text=text)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(json.loads(result.stdout),
                         {"columns": columns, "row_count": row_count})

    def test_counts_rows_and_lists_named_columns(self):
        self.assert_summary("name,score\nAda,10\nLin,2\n", ["name", "score"], 2)

    def test_quoted_commas_and_newlines_are_single_fields(self):
        self.assert_summary('name,note\n"Doe, Jane","first\nsecond"\n',
                            ["name", "note"], 1)

    def test_header_only_is_valid_zero_rows(self):
        self.assert_summary("name,score\n", ["name", "score"], 0)

    def test_crlf_and_escaped_quotes(self):
        self.assert_summary('name,note\r\nAda,"said ""hi"""\r\n',
                            ["name", "note"], 1)

    def test_blank_lines_do_not_count_as_rows(self):
        self.assert_summary("name\n\nAda\n\n", ["name"], 1)

    def test_unicode_is_supported(self):
        self.assert_summary("city,country\n東京,日本\n", ["city", "country"], 1)
