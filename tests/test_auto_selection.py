import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zcomp.profiles import PROFILE_ANY
from zcomp.strategy import CompressionStrategy


class AutoSelectionTests(unittest.TestCase):
    def test_store_wins_for_high_entropy(self):
        import os
        data = os.urandom(8192)
        result = CompressionStrategy().compress(PROFILE_ANY, data)
        self.assertEqual(result.algorithm_id, 0)

    def test_rle_candidate_selected_for_runs(self):
        data = b"A" * 2048
        result = CompressionStrategy().compress(PROFILE_ANY, data)
        self.assertIn(result.algorithm_id, {2, 3, 4, 5})


if __name__ == "__main__":
    unittest.main()
