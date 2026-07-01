"""Tests for the minimal data-acquisition demo."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from collector.collect import FIELDS, append_row, sample


class TestCollect(unittest.TestCase):
    def test_sample_has_expected_fields(self):
        self.assertEqual(set(sample()), set(FIELDS))

    def test_append_writes_header_then_rows(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "sub" / "samples.csv"
            append_row(out, sample())
            append_row(out, sample())
            lines = out.read_text().splitlines()
            self.assertEqual(lines[0], ",".join(FIELDS))
            self.assertEqual(len(lines), 3)  # header + 2 rows


if __name__ == "__main__":
    unittest.main()
