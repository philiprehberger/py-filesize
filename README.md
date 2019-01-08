# philiprehberger-filesize

Convert bytes to human-readable file sizes and back.

## Installation

```bash
pip install philiprehberger-filesize
```

## Usage

```python
from philiprehberger_filesize import humanize, parse, is_larger_than

humanize(1536)                  # "1.5 KB"
humanize(1073741824)            # "1.0 GB"
humanize(1024, binary=True)     # "1.0 KiB"

parse("1.5 GB")                 # 1500000000
parse("1 KiB")                  # 1024

is_larger_than(5000000, "1 MB") # True
```

## API

- `humanize(size, binary=False, precision=1)` — Bytes to human string
- `format_bytes(size, binary=False, precision=2)` — Alias with precision=2
- `parse(text)` — Human string to bytes
- `is_larger_than(size, threshold)` — Compare size to human string

## License

MIT
