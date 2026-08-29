import lzma

from .base import CodecResult


class LzmaCodec:
    algorithm_id = 4
    name = "LZMA"

    def compress(self, data: bytes) -> CodecResult:
        return CodecResult(payload=lzma.compress(data), metadata={})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        return lzma.decompress(payload)
