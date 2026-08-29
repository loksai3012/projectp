import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zcomp.archive import ZCArchive
from zcomp.errors import ArchiveError


class ArchiveValidationTests(unittest.TestCase):
    def test_bad_magic(self):
        with self.assertRaises(ArchiveError):
            ZCArchive().verify_and_extract(b"not-an-archive")

    def test_crc_mismatch(self):
        data = b"abcabcabc"
        blob = ZCArchive().create(
            source_filename="x.bin",
            file_type_id=255,
            algorithm_id=0,
            original_data=data,
            payload=data,
            codec_metadata={},
        )
        tampered = bytearray(blob)
        tampered[-1] ^= 0x01
        with self.assertRaises(ArchiveError):
            ZCArchive().verify_and_extract(bytes(tampered))


if __name__ == "__main__":
    unittest.main()
