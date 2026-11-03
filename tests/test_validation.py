import unittest

from tests.helpers import run_cli


class ValidationTests(unittest.TestCase):
    def assert_error(self, result, message):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "csv-toolkit: error: " + message + "\n")
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_column_is_concise_error(self):
        self.assert_error(run_cli("sort", "--column", "missing", text="name\nAda\n"),
                          "unknown column: missing")

    def test_duplicate_header_is_rejected(self):
        self.assert_error(run_cli("summary", text="name,name\nAda,Lin\n"),
                          "column names must be unique")

    def test_blank_header_name_is_rejected(self):
        self.assert_error(run_cli("summary", text="name, \nAda,2\n"),
                          "column names must not be blank")

    def test_short_row_is_rejected_before_output(self):
        self.assert_error(run_cli("sort", "--column", "score", text="name,score\nAda,2\nLin\n"),
                          "row 3 has 1 fields; expected 2")

    def test_long_row_is_rejected(self):
        self.assert_error(run_cli("summary", text="name\nAda,extra\n"),
                          "row 2 has 2 fields; expected 1")

    def test_unclosed_quote_is_concise_error(self):
        self.assert_error(run_cli("summary", text='name\n"unfinished\n'), "invalid CSV")

    def test_invalid_utf8_is_concise_error(self):
        import subprocess
        import sys
        from tests.helpers import ROOT
        result = subprocess.run([sys.executable, "-B", "-m", "csv_toolkit", "summary"],
                                input=b"name\n\xff\n", capture_output=True, cwd=ROOT, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertEqual(result.stderr, b"csv-toolkit: error: input must be UTF-8\n")
