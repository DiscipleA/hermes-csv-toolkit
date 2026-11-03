"""Execute the actual module with stdin; no shell or file output arguments."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*arguments, text=""):
    return subprocess.run(
        [sys.executable, "-B", "-m", "csv_toolkit", *arguments],
        input=text, text=True, encoding="utf-8", capture_output=True,
        cwd=ROOT, timeout=10,
    )
