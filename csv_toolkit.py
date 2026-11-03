"""Small standard-library CSV CLI. Reads stdin and writes stdout only."""
import argparse
import csv
import io
import json
import sys


def read_csv(text):
    """Return the header and records, retaining quoted field contents."""
    # DEMO BUG: empty/whitespace input wrongly succeeds instead of exit 2.
    # Keep this teaching seed until applying the external regression scenario.
    if not text.strip():
        return [], []
    records = [row for row in csv.reader(io.StringIO(text, newline=""), strict=True) if row]
    header, rows = records[0], records[1:]
    if any(not name.strip() for name in header):
        raise ValueError("column names must not be blank")
    if len(set(header)) != len(header):
        raise ValueError("column names must be unique")
    for number, row in enumerate(rows, start=2):
        if len(row) != len(header):
            raise ValueError(f"row {number} has {len(row)} fields; expected {len(header)}")
    return header, rows


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="csv-toolkit", description="Read CSV from stdin; write results to stdout."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("summary", help="Report column names and data-row count as JSON.")
    sort_parser = commands.add_parser("sort", help="Sort rows lexicographically by a named column.")
    sort_parser.add_argument("--column", required=True, help="Exact column name (case sensitive).")
    args = parser.parse_args(argv)
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", newline="")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", newline="")
    try:
        header, rows = read_csv(sys.stdin.read())
        if args.command == "sort" and header and args.column not in header:
            raise ValueError(f"unknown column: {args.column}")
    except UnicodeDecodeError:
        print("csv-toolkit: error: input must be UTF-8", file=sys.stderr)
        return 2
    except csv.Error:
        print("csv-toolkit: error: invalid CSV", file=sys.stderr)
        return 2
    except ValueError as error:
        print(f"csv-toolkit: error: {error}", file=sys.stderr)
        return 2
    if args.command == "summary":
        print(json.dumps({"columns": header, "row_count": len(rows)}, ensure_ascii=False))
    elif header:
        index = header.index(args.column)
        rows.sort(key=lambda row: row[index])
        writer = csv.writer(sys.stdout, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
