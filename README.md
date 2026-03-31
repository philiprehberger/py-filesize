# philiprehberger-filesize

[![Tests](https://github.com/philiprehberger/py-filesize/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-filesize/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-filesize.svg)](https://pypi.org/project/philiprehberger-filesize/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-filesize)](https://github.com/philiprehberger/py-filesize/commits/main)

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

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-filesize)

🐛 [Report issues](https://github.com/philiprehberger/py-filesize/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-filesize/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
