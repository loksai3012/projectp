from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

from .codecs import ALGORITHMS, create_codec
from .errors import ArchiveError

MAGIC = b"ZC"
VERSION = 1

# <2sBBBBQIHIQ
# magic, version, file_type_id, algorithm_id, flags,
# original_size, crc32, filename_len, metadata_len, payload_len
_HEADER = struct.Struct("<2sBBBBQIHIQ")


class ZCArchive:
    def create(
        self,
        *,
        source_filename: str,
        file_type_id: int,
        algorithm_id: int,
        original_data: bytes,
        payload: bytes,
        codec_metadata: dict | None = None,
        flags: int = 0,
    ) -> bytes:
        safe_name = Path(source_filename).name
        filename_bytes = safe_name.encode("utf-8")
        metadata_bytes = json.dumps(codec_metadata or {}, separators=(",", ":")).encode("utf-8")
        original_size = len(original_data)
        crc = zlib.crc32(original_data) & 0xFFFFFFFF

        header = _HEADER.pack(
            MAGIC,
            VERSION,
            file_type_id,
            algorithm_id,
            flags,
            original_size,
            crc,
            len(filename_bytes),
            len(metadata_bytes),
            len(payload),
        )
        return header + filename_bytes + metadata_bytes + payload

    def parse(self, blob: bytes) -> dict:
        if len(blob) < _HEADER.size:
            raise ArchiveError("Invalid Zero-Compress archive.")

        (
            magic,
            version,
            file_type_id,
            algorithm_id,
            flags,
            original_size,
            crc,
            filename_len,
            metadata_len,
            payload_len,
        ) = _HEADER.unpack(blob[: _HEADER.size])

        if magic != MAGIC:
            raise ArchiveError("Invalid Zero-Compress archive.")
        if version != VERSION:
            raise ArchiveError("Unsupported archive version.")
        if algorithm_id not in ALGORITHMS:
            raise ArchiveError("Unknown compression algorithm.")

        pos = _HEADER.size
        end_name = pos + filename_len
        end_meta = end_name + metadata_len
        end_payload = end_meta + payload_len

        if end_payload != len(blob):
            raise ArchiveError("Unexpected end of archive.")

        try:
            filename = blob[pos:end_name].decode("utf-8")
        except UnicodeDecodeError as e:
            raise ArchiveError("Invalid metadata.") from e

        try:
            metadata = json.loads(blob[end_name:end_meta].decode("utf-8"))
            if not isinstance(metadata, dict):
                raise ValueError("metadata must be object")
        except Exception as e:
            raise ArchiveError("Invalid metadata.") from e

        payload = blob[end_meta:end_payload]

        return {
            "version": version,
            "file_type_id": file_type_id,
            "algorithm_id": algorithm_id,
            "flags": flags,
            "original_size": original_size,
            "crc": crc,
            "filename": Path(filename).name or "output.bin",
            "metadata": metadata,
            "payload": payload,
        }

    def verify_and_extract(self, blob: bytes) -> tuple[str, bytes]:
        parsed = self.parse(blob)
        codec = create_codec(parsed["algorithm_id"])

        try:
            data = codec.decompress(
                parsed["payload"], parsed["metadata"], parsed["original_size"]
            )
        except Exception as e:
            raise ArchiveError("Invalid Zero-Compress archive.") from e

        if len(data) != parsed["original_size"]:
            raise ArchiveError("Decompressed size mismatch.")

        crc = zlib.crc32(data) & 0xFFFFFFFF
        if crc != parsed["crc"]:
            raise ArchiveError("CRC verification failed.")

        return parsed["filename"], data
