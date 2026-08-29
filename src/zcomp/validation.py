from __future__ import annotations

from pathlib import Path

from .errors import ValidationError
from .profiles import PROFILE_ANY, Profile


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PDF_MAGIC = b"%PDF-"
JPEG_MAGIC = b"\xff\xd8\xff"


def validate_selection(path: Path, profile: Profile) -> None:
    if not path.exists():
        raise ValidationError("Selected path does not exist.")
    if not path.is_file():
        raise ValidationError("Selected path is not a regular file.")

    if profile is PROFILE_ANY:
        return

    ext = path.suffix.lower()
    if ext not in profile.extensions:
        expected = ", ".join(profile.extensions)
        raise ValidationError(
            f"Invalid file type. Expected {profile.key} ({expected}), selected {path.name}."
        )

    # Optional lightweight signatures.
    head = path.read_bytes()[:16]
    if profile.key == "PNG" and head and not head.startswith(PNG_MAGIC):
        raise ValidationError("Invalid PNG signature.")
    if profile.key == "PDF" and head and not head.startswith(PDF_MAGIC):
        raise ValidationError("Invalid PDF signature.")
    if profile.key == "JPEG" and head and not head.startswith(JPEG_MAGIC):
        raise ValidationError("Invalid JPEG signature.")
