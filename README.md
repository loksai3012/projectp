# Zero-Compress: Format-Aware Lossless Compression

Zero-Compress is a zero-dependency Python compression suite that stores data in a custom `.zc` archive and restores files byte-for-byte.

## Features

- Interactive CLI:
  - Compress
  - Decompress
  - Exit
- Format profiles:
  - TXT, PDF, PNG, JPEG, MP4, Any File Type
- Profile-aware strategy:
  - Preset-first for known formats
  - `STORE` fallback when compression is not smaller
  - Auto mode candidate comparison for Any File Type
- Custom `.zc` archive:
  - Magic + version
  - File type ID + algorithm ID
  - Original size + CRC32
  - Safe basename + codec metadata + payload
- Integrity checks on extract:
  - Header and boundary validation
  - Decompressed size check
  - CRC verification
- Collision-safe output naming in Downloads

## Algorithms

- `0` STORE
- `1` HUFFMAN
- `2` RLE
- `3` ZLIB
- `4` LZMA
- `5` ZSTD (with stdlib fallback where unavailable)

## Run

```bash
python run.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

- `src/zcomp/cli.py` - interactive workflow
- `src/zcomp/profiles.py` - profile table
- `src/zcomp/strategy.py` - codec selection logic
- `src/zcomp/archive.py` - `.zc` archive pack/unpack + verification
- `src/zcomp/validation.py` - file and signature checks
- `src/zcomp/codecs/` - codec adapters
- `tests/` - unit tests for round-trip, auto mode, and validation
