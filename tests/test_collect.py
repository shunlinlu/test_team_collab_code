"""Tests for the minimal data-acquisition demo."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from collector import collect


class TestCollect(unittest.TestCase):
    def test_sample_has_expected_fields(self):
        self.assertEqual(set(collect.sample()), set(collect.FIELDS))

    def test_sample_rounds_supported_load_average(self):
        with mock.patch.object(collect.os, "getloadavg", return_value=(1.2345, 2.3456, 3.4567), create=True):
            row = collect.sample()
        self.assertEqual(row["load1"], 1.234)
        self.assertEqual(row["load5"], 2.346)
        self.assertEqual(row["load15"], 3.457)

    def test_sample_uses_zero_fallback_without_getloadavg(self):
        with mock.patch.object(collect.os, "getloadavg", None, create=True):
            row = collect.sample()
        self.assertEqual(row["load1"], 0.0)
        self.assertEqual(row["load5"], 0.0)
        self.assertEqual(row["load15"], 0.0)

    def test_append_writes_header_then_rows(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "sub" / "samples.csv"
            collect.append_row(out, collect.sample())
            collect.append_row(out, collect.sample())
            lines = out.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], ",".join(collect.FIELDS))
            self.assertEqual(len(lines), 3)  # header + 2 rows


if __name__ == "__main__":
    unittest.main()
