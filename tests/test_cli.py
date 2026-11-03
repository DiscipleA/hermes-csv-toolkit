import unittest

from tests.helpers import run_cli


class CliTests(unittest.TestCase):
    def test_main_help_lists_commands(self):
        result = run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("summary", result.stdout)
        self.assertIn("sort", result.stdout)

    def test_sort_help_documents_named_column(self):
        result = run_cli("sort", "--help")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("--column", result.stdout)

    def test_missing_column_option_is_usage_error(self):
        result = run_cli("sort", text="name\nAda\n")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("--column", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_no_file_output_option_is_supported(self):
        result = run_cli("summary", "--output", "must-not-exist.csv", text="name\nAda\n")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unrecognized arguments", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
