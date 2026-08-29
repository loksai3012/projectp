from .base import Codec, CodecResult
from .store import StoreCodec
from .huffman import HuffmanCodec
from .rle import RLECodec
from .zlib_codec import ZlibCodec
from .lzma_codec import LzmaCodec
from .zstd_codec import ZstdCodec

ALGORITHMS = {
    0: StoreCodec,
    1: HuffmanCodec,
    2: RLECodec,
    3: ZlibCodec,
    4: LzmaCodec,
    5: ZstdCodec,
}

ALGORITHM_NAMES = {
    0: "STORE",
    1: "HUFFMAN",
    2: "RLE",
    3: "ZLIB",
    4: "LZMA",
    5: "ZSTD",
}


def create_codec(algorithm_id: int) -> Codec:
    cls = ALGORITHMS.get(algorithm_id)
    if cls is None:
        raise KeyError(algorithm_id)
    return cls()
