# Changelog

## 0.3.0 (2026-05-30)

- Add `total()` for summing byte counts from mixed int and human-readable inputs
- Add `compare(a, b)` returning -1/0/1 after parsing — handy for sorting mixed size values

## 0.2.0 (2026-04-28)

- Add `to_unit(size, unit)` — convert bytes to a specific named unit returning a float (case-insensitive, accepts SI and binary units)
- Add exported size constants: `BYTES`, `KB`, `MB`, `GB`, `TB`, `KIB`, `MIB`, `GIB`, `TIB`
- Fix `pyproject.toml` description to end with a period (matches README)
- Reformat malformed earlier CHANGELOG headings

## 0.1.6 (2026-04-01)

- Standardize README structure and fix compliance issues

## 0.1.5 (2026-03-31)

- Add pytest and mypy tool configuration to pyproject.toml
- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.4

- Add Development section to README

## 0.1.1

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)

- Initial release
