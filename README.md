# hermes-csv-toolkit

A small, AI-assisted teaching repository: a standard-library Python CLI that reads
UTF-8 CSV from stdin and writes JSON summaries or sorted CSV to stdout. No packages,
network access, credentials, file-path inputs, or file-output options are needed.

## Run

Requires Python 3.10+; verified locally with Python 3.14.7. Run from this directory.
These examples use Bash (including Git Bash on Windows):

```bash
python -B -m csv_toolkit --help
python -B -m csv_toolkit summary < examples/demo.csv
python -B -m csv_toolkit sort --column score < examples/demo.csv
printf 'name,score\nAda,10\nLin,2\n' | python -B -m csv_toolkit summary
```

The summary of `examples/demo.csv` is:

```json
{"columns": ["name", "score", "note"], "row_count": 3}
```

Sorting by `score` yields Zoe (1), Ada (10), then Lin (2): the baseline sorts strings,
**not numbers**. Sorting is stable, ascending, case-sensitive, and uses exact header
names. CSV quoting, embedded newlines, escaped double quotes, Unicode, and CRLF
inputs are supported. Output uses LF line endings and UTF-8. The header is kept;
header-only input is valid with zero data rows. Completely blank lines are ignored.
Duplicate/blank column names, ragged rows, invalid UTF-8, malformed quoted input,
and unknown sort columns produce exit 2 with a concise stderr diagnostic and no
stdout. Reported row numbers count CSV records, excluding skipped blank lines,
not physical lines when quoted fields contain newlines. Argparse handles usage
errors and help; usage errors may include usage text.

The CLI never opens an output file. If you choose shell redirection, never redirect
to the same input file: the shell can truncate it before Python starts.

## Test

```bash
python -B -m unittest discover -v
```

The supported baseline has **22 passing tests**, using real subprocess invocations.
No dependency installation is required. `-B` avoids bytecode cache artifacts.

## Deliberate teaching defect and presentation seeds

**This is a demo, not a production CSV validation library.** An intentional, marked
`DEMO BUG` in `csv_toolkit.py` treats entirely empty or whitespace-only stdin as
successful empty data. `summary` returns empty columns and zero rows; `sort`
returns no output. Both incorrectly exit 0. Do not accidentally present this as
correct behavior or silently fix it before the bug-fix demonstration.

The two local presentation seeds live outside this repository at
`../../scenarios/hermes-csv-toolkit/`:

1. `bugfix.md` and `test_regression.py`: copy the regression into a disposable
   repository copy's `tests/`, reproduce the failure, then implement a clean error.
2. `enhancement.md`: an optional `sort --numeric` feature with explicit acceptance
   criteria. The baseline intentionally does not implement that option.

The repository includes a GitHub Actions test workflow. The demonstration issues
and PRs live on GitHub; Hermes maintenance jobs and credentials are configured
separately on the presenter's machine, never committed here.

## Demonstration limits and AI disclosure

Generated with AI assistance and exercised locally; review changes and rerun tests
before presenting or adapting it. It reads the entire input into memory, supports
comma-separated CSV only, and does not promise production-grade parsing, streaming,
locale-aware ordering, schema inference, Excel formula sanitization, or numeric
sorting. Keep real or sensitive datasets out of demonstrations. Existing tests
cover the documented baseline, not every possible CSV dialect or operating system.
