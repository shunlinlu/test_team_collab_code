#!/usr/bin/env python3
"""Minimal data-acquisition (数采) demo.

Periodically samples host load average and appends each reading to a CSV file.
Standard library only; runs on macOS and Linux.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ["timestamp", "load1", "load5", "load15"]


def sample() -> dict:
    """Take one reading of the host's 1/5/15-minute load averages."""
    load1, load5, load15 = os.getloadavg()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "load1": round(load1, 3),
        "load5": round(load5, 3),
        "load15": round(load15, 3),
    }


def append_row(path: Path, row: dict) -> None:
    """Append one row to the CSV at `path`, writing a header if the file is new."""
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Sample host load into a CSV.")
    parser.add_argument("--out", type=Path, default=Path("data/samples.csv"),
                        help="output CSV path (default: data/samples.csv)")
    parser.add_argument("--count", type=int, default=5,
                        help="number of samples to take (default: 5)")
    parser.add_argument("--interval", type=float, default=1.0,
                        help="seconds between samples (default: 1.0)")
    args = parser.parse_args(argv)

    for i in range(args.count):
        row = sample()
        append_row(args.out, row)
        print(f"[{i + 1}/{args.count}] {row}")
        if i < args.count - 1:
            time.sleep(args.interval)
    print(f"wrote {args.count} samples -> {args.out}")


if __name__ == "__main__":
    main()
