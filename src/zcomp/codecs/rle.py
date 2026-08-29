from .base import CodecResult
from ..errors import CodecError


class RLECodec:
    algorithm_id = 2
    name = "RLE"

    def compress(self, data: bytes) -> CodecResult:
        if not data:
            return CodecResult(payload=b"", metadata={})
        out = bytearray()
        prev = data[0]
        count = 1
        for b in data[1:]:
            if b == prev and count < 255:
                count += 1
            else:
                out.append(count)
                out.append(prev)
                prev = b
                count = 1
        out.append(count)
        out.append(prev)
        return CodecResult(payload=bytes(out), metadata={})

    def decompress(self, payload: bytes, metadata: dict, original_size: int) -> bytes:
        out = bytearray()
        it = iter(payload)
        for c in it:
            try:
                b = next(it)
            except StopIteration as e:
                raise CodecError("Invalid RLE payload") from e
            out.extend(bytes([b]) * c)
        return bytes(out)
