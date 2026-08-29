from .base import CodecResult


class StoreCodec:
    algorithm_id = 0
    name = "STORE"

    def compress(self, data: bytes) -> CodecResult:
        return CodecResult(payload=data, metadata={})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        return payload
