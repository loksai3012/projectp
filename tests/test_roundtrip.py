import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zcomp.archive import ZCArchive
from zcomp.profiles import PROFILE_TXT
from zcomp.strategy import CompressionStrategy


class RoundTripTests(unittest.TestCase):
    def test_txt_roundtrip(self):
        data = (b"hello world\n" * 400) + b"tail"
        strategy = CompressionStrategy()
        result = strategy.compress(PROFILE_TXT, data)

        blob = ZCArchive().create(
            source_filename="report.txt",
            file_type_id=PROFILE_TXT.file_type_id,
            algorithm_id=result.algorithm_id,
            original_data=data,
            payload=result.payload,
            codec_metadata=result.codec_metadata,
        )

        name, out = ZCArchive().verify_and_extract(blob)
        self.assertEqual(name, "report.txt")
        self.assertEqual(out, data)


if __name__ == "__main__":
    unittest.main()
