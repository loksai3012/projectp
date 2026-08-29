import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from zcomp.errors import ValidationError
from zcomp.profiles import PROFILE_ANY, PROFILE_PNG, PROFILE_TXT
from zcomp.validation import validate_selection


class FileValidationTests(unittest.TestCase):
    def test_txt_extension_required(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "a.bin"
            p.write_bytes(b"abc")
            with self.assertRaises(ValidationError):
                validate_selection(p, PROFILE_TXT)

    def test_png_signature_validation(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "img.png"
            p.write_bytes(b"BADPNG")
            with self.assertRaises(ValidationError):
                validate_selection(p, PROFILE_PNG)

    def test_any_accepts_regular_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "unknown.bin"
            p.write_bytes(b"abc")
            validate_selection(p, PROFILE_ANY)


if __name__ == "__main__":
    unittest.main()
