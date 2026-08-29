from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CodecResult:
    payload: bytes
    metadata: dict


class Codec(Protocol):
    algorithm_id: int
    name: str

    def compress(self, data: bytes) -> CodecResult: ...

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes: ...
