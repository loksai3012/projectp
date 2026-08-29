from __future__ import annotations

from pathlib import Path

from .archive import ZCArchive
from .codecs import ALGORITHM_NAMES
from .errors import ArchiveError, ValidationError
from .file_dialog import select_file_for_compress, select_file_for_decompress
from .filesystem import downloads_path, safe_output_path
from .profiles import PROFILE_ANY, PROFILE_MENU, detect_profile_by_extension
from .strategy import CompressionStrategy, algorithm_label
from .validation import validate_selection


class Application:
    def __init__(self) -> None:
        self.archive = ZCArchive()
        self.strategy = CompressionStrategy()

    def run(self) -> None:
        print("========================================")
        print(" ZERO-COMPRESS - FORMAT-AWARE LOSSLESS ")
        print("========================================")
        while True:
            print("\nWhat do you want to do?")
            print("1. Compress")
            print("2. Decompress")
            print("3. Exit")
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.compress_flow()
            elif choice == "2":
                self.decompress_flow()
            elif choice == "3":
                print("Goodbye")
                return
            else:
                print("Invalid choice")

    def _select_profile(self):
        print("\nSelect the type of file you want to compress:")
        print("1. Text (.txt)")
        print("2. PDF (.pdf)")
        print("3. PNG (.png)")
        print("4. JPEG (.jpg/.jpeg)")
        print("5. MP4 (.mp4)")
        print("6. Any File Type")
        while True:
            choice = input("Profile: ").strip()
            profile = PROFILE_MENU.get(choice)
            if profile:
                return profile
            print("Invalid profile choice.")

    def compress_flow(self) -> None:
        profile = self._select_profile()
        selected = self._retry_select_compress(profile)
        if selected is None:
            return

        data = selected.read_bytes()
        if profile is PROFILE_ANY:
            detected = detect_profile_by_extension(selected)
            print(f"Detected type: {selected.suffix or '(none)'}")
            print("Mode: Auto selection")

        result = self.strategy.compress(profile, data)
        archive_bytes = self.archive.create(
            source_filename=selected.name,
            file_type_id=profile.file_type_id,
            algorithm_id=result.algorithm_id,
            original_data=data,
            payload=result.payload,
            codec_metadata=result.codec_metadata,
        )

        out_path = safe_output_path(downloads_path(), selected.with_suffix(".zc").name)
        out_path.write_bytes(archive_bytes)

        print("\nCandidate sizes:")
        for alg_id, size in result.candidate_sizes:
            print(f"  {algorithm_label(alg_id):8} {size} bytes")
        print(f"Selected: {ALGORITHM_NAMES.get(result.algorithm_id, result.algorithm_id)}")
        print(f"Original size: {len(data)} bytes")
        print(f"Archive size: {len(archive_bytes)} bytes")
        print(f"Saved: {out_path}")

    def _retry_select_compress(self, profile):
        while True:
            selected = select_file_for_compress(profile)
            if selected is None:
                print("No file selected.")
                return None
            try:
                validate_selection(selected, profile)
                return selected
            except ValidationError as e:
                print(f"\n{e}")
                again = input("Select another file? [Y/N] ").strip().lower()
                if again != "y":
                    return None

    def decompress_flow(self) -> None:
        selected = self._retry_select_archive()
        if selected is None:
            return

        try:
            filename, data = self.archive.verify_and_extract(selected.read_bytes())
        except ArchiveError as e:
            print(e)
            return

        out_path = safe_output_path(downloads_path(), Path(filename).name)
        out_path.write_bytes(data)
        print(f"Decompressed and saved to: {out_path}")

    def _retry_select_archive(self):
        while True:
            selected = select_file_for_decompress()
            if selected is None:
                print("No file selected.")
                return None
            if selected.suffix.lower() == ".zc":
                return selected
            print("Invalid file type. Please select a .zc archive.")
            again = input("Select another file? [Y/N] ").strip().lower()
            if again != "y":
                return None


def main() -> None:
    Application().run()


if __name__ == "__main__":
    main()
