import zlib

from .base import CodecResult


class ZstdCodec:
    algorithm_id = 5
    name = "ZSTD"

    def compress(self, data: bytes) -> CodecResult:
        try:
            import compression.zstd as zstd  # type: ignore[attr-defined]

            if hasattr(zstd, "compress"):
                return CodecResult(payload=zstd.compress(data), metadata={"impl": "compression.zstd"})
        except Exception:
            pass
        return CodecResult(payload=zlib.compress(data), metadata={"impl": "zlib-fallback"})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        impl = metadata.get("impl", "compression.zstd")
        if impl == "zlib-fallback":
            return zlib.decompress(payload)
        try:
            import compression.zstd as zstd  # type: ignore[attr-defined]

            if hasattr(zstd, "decompress"):
                return zstd.decompress(payload)
        except Exception:
            pass
        return zlib.decompress(payload)
