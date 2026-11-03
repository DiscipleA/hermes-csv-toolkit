"""Copy this file to tests/test_regression.py in a disposable repository copy."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EmptyInputRegressionTests(unittest.TestCase):
    def assert_clean_empty_error(self, text):
        for arguments in (("summary",), ("sort", "--column", "name")):
            with self.subTest(arguments=arguments, text=repr(text)):
                result = subprocess.run(
                    [sys.executable, "-B", "-m", "csv_toolkit", *arguments],
                    input=text, text=True, encoding="utf-8", capture_output=True,
                    cwd=ROOT, timeout=10,
                )
                self.assertEqual(result.returncode, 2, repr(result))
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "csv-toolkit: error: input is empty\n")
                self.assertNotIn("Traceback", result.stderr)

    def test_entirely_empty_input_is_a_clean_user_error(self):
        self.assert_clean_empty_error("")

    def test_whitespace_only_input_is_a_clean_user_error(self):
        self.assert_clean_empty_error(" \t\r\n  \n")
