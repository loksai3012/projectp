from collections import Counter

from ..huffman import HuffmanCodec as CoreHuffmanCodec
from .base import CodecResult


class HuffmanCodec:
    algorithm_id = 1
    name = "HUFFMAN"

    def __init__(self) -> None:
        self._core = CoreHuffmanCodec()

    def compress(self, data: bytes) -> CodecResult:
        payload, freq = self._core.encode(data)
        return CodecResult(payload=payload, metadata={"freq": {str(k): v for k, v in freq.items()}})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        freq = {int(k): int(v) for k, v in metadata.get("freq", {}).items()}
        if not freq and original_size == 0:
            return b""
        return self._core.decode(payload, freq, original_size)
