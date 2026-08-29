import zlib

from .base import CodecResult


class ZlibCodec:
    algorithm_id = 3
    name = "ZLIB"

    def compress(self, data: bytes) -> CodecResult:
        return CodecResult(payload=zlib.compress(data), metadata={})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        return zlib.decompress(payload)
