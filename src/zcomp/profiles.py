from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Profile:
    key: str
    display_name: str
    file_type_id: int
    extensions: tuple[str, ...]
    primary_algorithm: int | None
    candidates: tuple[int, ...]


PROFILE_TXT = Profile("TXT", "Text (.txt)", 1, (".txt",), 5, (5, 4, 3, 1, 2, 0))
PROFILE_PDF = Profile("PDF", "PDF (.pdf)", 2, (".pdf",), 5, (5, 4, 3, 1, 0))
PROFILE_PNG = Profile("PNG", "PNG (.png)", 3, (".png",), 5, (5, 0))
PROFILE_JPEG = Profile("JPEG", "JPEG (.jpg/.jpeg)", 4, (".jpg", ".jpeg"), 5, (5, 0))
PROFILE_MP4 = Profile("MP4", "MP4 (.mp4)", 5, (".mp4",), 5, (5, 0))
PROFILE_ANY = Profile("ANY", "Any File Type", 255, tuple(), None, (5, 4, 3, 1, 2, 0))

PROFILE_MENU = {
    "1": PROFILE_TXT,
    "2": PROFILE_PDF,
    "3": PROFILE_PNG,
    "4": PROFILE_JPEG,
    "5": PROFILE_MP4,
    "6": PROFILE_ANY,
}

ALL_PROFILES = tuple(PROFILE_MENU.values())


def detect_profile_by_extension(path: Path) -> Profile:
    ext = path.suffix.lower()
    for profile in ALL_PROFILES:
        if ext in profile.extensions:
            return profile
    return PROFILE_ANY
