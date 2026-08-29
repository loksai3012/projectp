from __future__ import annotations

from pathlib import Path
from tkinter import Tk, filedialog

from .profiles import PROFILE_ANY, Profile


def _ask_file_dialog(title: str, filetypes=None) -> Path | None:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        selected = filedialog.askopenfilename(title=title, filetypes=filetypes)
    finally:
        root.destroy()
    if not selected:
        return None
    return Path(selected)


def filetypes_for_profile(profile: Profile):
    if profile is PROFILE_ANY:
        return [("All files", "*.*")]
    patterns = " ".join(f"*{ext}" for ext in profile.extensions)
    return [(profile.display_name, patterns), ("All files", "*.*")]


def select_file_for_compress(profile: Profile) -> Path | None:
    return _ask_file_dialog("Select file to compress", filetypes_for_profile(profile))


def select_file_for_decompress() -> Path | None:
    return _ask_file_dialog("Select .zc archive to decompress", [("Zero-Compress", "*.zc"), ("All files", "*.*")])
