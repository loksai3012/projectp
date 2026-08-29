# STDLIB Usage Map

This project uses Python standard library only.

## Core runtime

- `pathlib` - file paths and basename handling
- `os` / `sys` - environment and path setup
- `tkinter.filedialog` - native file picker dialogs
- `json` - metadata encoding in `.zc`
- `struct` - fixed-width archive header
- `zlib` - CRC32 and zlib codec
- `lzma` - LZMA codec
- `collections.Counter` + `heapq` - Huffman implementation

## Optional stdlib feature

- `compression.zstd` - preferred ZSTD adapter when available (Python 3.14+)

## Quality and tests

- `unittest` - test framework
- `tempfile` - temporary files in tests

## Dependency policy

- `requirements.txt` is intentionally empty
- No third-party runtime dependencies are required
