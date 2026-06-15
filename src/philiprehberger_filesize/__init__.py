"""Convert bytes to human-readable file sizes and back."""

from __future__ import annotations

import re


__all__ = [
    "humanize",
    "parse",
    "format_bytes",
    "from_unit",
    "is_larger_than",
    "to_unit",
    "total",
    "compare",
    "BYTES",
    "KB",
    "MB",
    "GB",
    "TB",
    "KIB",
    "MIB",
    "GIB",
    "TIB",
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

BYTES = 1
KB = 1000
MB = 1000**2
GB = 1000**3
TB = 1000**4
KIB = 1024
MIB = 1024**2
GIB = 1024**3
TIB = 1024**4


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


def to_unit(size: int | float, unit: str) -> float:
    """Convert a byte count to a specific named unit, returning a float.

    Useful when you need a numeric value rather than a formatted string.
    Accepts SI (``"KB"``, ``"MB"``) and binary (``"KiB"``, ``"MiB"``) units.

    Args:
        size: Size in bytes.
        unit: Target unit name (case-insensitive). One of
            ``"B"``, ``"KB"``, ``"MB"``, ``"GB"``, ``"TB"``, ``"PB"``, ``"EB"``,
            ``"KiB"``, ``"MiB"``, ``"GiB"``, ``"TiB"``, ``"PiB"``, ``"EiB"``.

    Returns:
        Size converted to the target unit.

    Raises:
        ValueError: If *unit* is not recognized.
    """
    key = unit.lower().strip()
    if key not in _UNIT_MULTIPLIERS:
        raise ValueError(f"Unknown unit: '{unit}'")
    return float(size) / _UNIT_MULTIPLIERS[key]


def from_unit(value: int | float, unit: str) -> int:
    """Convert a numeric value in a named unit to bytes.

    Inverse of :func:`to_unit`. Accepts SI (``"KB"``, ``"MB"``) and binary
    (``"KiB"``, ``"MiB"``) units; case-insensitive.

    Args:
        value: Numeric value in the source unit.
        unit: Source unit name.

    Returns:
        Size in bytes (integer).

    Raises:
        ValueError: If *unit* is not recognized.
    """
    key = unit.lower().strip()
    if key not in _UNIT_MULTIPLIERS:
        raise ValueError(f"Unknown unit: '{unit}'")
    return int(value * _UNIT_MULTIPLIERS[key])


def is_larger_than(size: int | float, threshold: str) -> bool:
    """Check if a byte size exceeds a human-readable threshold.

    Args:
        size: Size in bytes.
        threshold: Human-readable size string (e.g., ``"100 MB"``).

    Returns:
        True if *size* exceeds the parsed threshold.
    """
    return size > parse(threshold)


def total(*sizes: int | str) -> int:
    """Sum byte counts, accepting plain ints and human-readable strings.

    String values are parsed via :func:`parse`. Returns the total as an int.

    Args:
        *sizes: Any mix of ``int`` byte counts and human-readable size strings.

    Returns:
        Sum of all sizes in bytes.

    Raises:
        TypeError: If an argument is neither ``int`` nor ``str``.
        ValueError: If a string argument cannot be parsed.
    """
    result = 0
    for item in sizes:
        if isinstance(item, bool):
            # bool is a subclass of int; reject to avoid silent surprises.
            msg = f"Unsupported type for total(): {type(item).__name__}"
            raise TypeError(msg)
        if isinstance(item, int):
            result += item
        elif isinstance(item, str):
            result += parse(item)
        else:
            msg = f"Unsupported type for total(): {type(item).__name__}"
            raise TypeError(msg)
    return result


def compare(a: int | str, b: int | str) -> int:
    """Return -1, 0, or 1 after parsing both operands.

    Strings are normalized via :func:`parse` so mixed int/string size values can
    be compared directly. Suitable as a building block for sorting mixed sizes.

    Args:
        a: First size, as ``int`` bytes or human-readable string.
        b: Second size, as ``int`` bytes or human-readable string.

    Returns:
        ``-1`` if ``a < b``, ``0`` if equal, ``1`` if ``a > b``.
    """
    left = parse(a) if isinstance(a, str) else int(a)
    right = parse(b) if isinstance(b, str) else int(b)
    return (left > right) - (left < right)
