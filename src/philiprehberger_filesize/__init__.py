"""Convert bytes to human-readable file sizes and back."""

from __future__ import annotations

import re


__all__ = [
    "humanize",
    "parse",
    "format_bytes",
    "is_larger_than",
]

_SI_UNITS = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
_BINARY_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]

_PARSE_RE = re.compile(r"^\s*([\d.]+)\s*([A-Za-z]*)\s*$")

_UNIT_MULTIPLIERS: dict[str, int] = {
    "b": 1,
    "kb": 1000,
    "mb": 1000**2,
    "gb": 1000**3,
    "tb": 1000**4,
    "pb": 1000**5,
    "eb": 1000**6,
    "kib": 1024,
    "mib": 1024**2,
    "gib": 1024**3,
    "tib": 1024**4,
    "pib": 1024**5,
    "eib": 1024**6,
}


def humanize(size: int | float, *, binary: bool = False, precision: int = 1) -> str:
    """Convert bytes to a human-readable string.

    Args:
        size: Size in bytes.
        binary: Use binary units (KiB, MiB) instead of SI (KB, MB).
        precision: Decimal places.

    Returns:
        Formatted string like ``"1.5 MB"`` or ``"1.5 MiB"``.
    """
    units = _BINARY_UNITS if binary else _SI_UNITS
    base = 1024 if binary else 1000
    value = float(size)

    for unit in units[:-1]:
        if abs(value) < base:
            if unit == "B":
                return f"{int(value)} B"
            return f"{value:.{precision}f} {unit}"
        value /= base

    return f"{value:.{precision}f} {units[-1]}"


def format_bytes(size: int | float, *, binary: bool = False, precision: int = 2) -> str:
    """Alias for :func:`humanize` with default precision of 2.

    Args:
        size: Size in bytes.
        binary: Use binary units.
        precision: Decimal places.

    Returns:
        Formatted string.
    """
    return humanize(size, binary=binary, precision=precision)


def parse(text: str) -> int:
    """Parse a human-readable size string back to bytes.

    Accepts formats like ``"1.5 GB"``, ``"500 KiB"``, ``"1024"``.

    Args:
        text: Human-readable size string.

    Returns:
        Size in bytes (integer).

    Raises:
        ValueError: If the string cannot be parsed.
    """
    match = _PARSE_RE.match(text.strip())
    if not match:
        msg = f"Cannot parse size: '{text}'"
        raise ValueError(msg)

    number = float(match.group(1))
    unit = match.group(2).strip()

    if not unit:
        return int(number)

    key = unit.lower()
    if key not in _UNIT_MULTIPLIERS:
        msg = f"Unknown unit: '{unit}'"
        raise ValueError(msg)

    return int(number * _UNIT_MULTIPLIERS[key])


def is_larger_than(size: int | float, threshold: str) -> bool:
    """Check if a byte size exceeds a human-readable threshold.

    Args:
        size: Size in bytes.
        threshold: Human-readable size string (e.g., ``"100 MB"``).

    Returns:
        True if *size* exceeds the parsed threshold.
    """
    return size > parse(threshold)
