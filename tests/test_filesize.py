import pytest
from philiprehberger_filesize import (
    GB,
    KB,
    MB,
    MIB,
    compare,
    format_bytes,
    from_unit,
    humanize,
    is_larger_than,
    parse,
    to_unit,
    total,
)


def test_humanize_bytes():
    assert humanize(500) == "500 B"


def test_humanize_kb():
    assert humanize(1500) == "1.5 KB"


def test_humanize_mb():
    assert humanize(1_500_000) == "1.5 MB"


def test_humanize_gb():
    assert humanize(1_500_000_000) == "1.5 GB"


def test_humanize_binary():
    assert humanize(1024, binary=True) == "1.0 KiB"


def test_humanize_precision():
    assert humanize(1536, precision=2) == "1.54 KB"


def test_format_bytes_default_precision():
    result = format_bytes(1536)
    assert "1.54" in result


def test_parse_kb():
    assert parse("1.5 KB") == 1500


def test_parse_mb():
    assert parse("1 MB") == 1_000_000


def test_parse_gib():
    assert parse("1 GiB") == 1024**3


def test_parse_plain_number():
    assert parse("1024") == 1024


def test_parse_invalid():
    with pytest.raises(ValueError):
        parse("not a size")


def test_parse_unknown_unit():
    with pytest.raises(ValueError):
        parse("5 XB")


def test_is_larger_than():
    assert is_larger_than(5_000_000, "1 MB") is True
    assert is_larger_than(500, "1 MB") is False


def test_zero():
    assert humanize(0) == "0 B"


def test_round_trip():
    original = 1_500_000
    text = humanize(original)
    parsed = parse(text)
    assert abs(parsed - original) < 100_000  # approximate due to rounding


def test_to_unit_kb():
    assert to_unit(1500, "KB") == 1.5


def test_to_unit_mib():
    assert to_unit(1024 * 1024, "MiB") == 1.0


def test_to_unit_case_insensitive():
    assert to_unit(1000, "kb") == 1.0
    assert to_unit(1000, "KB") == 1.0


def test_to_unit_unknown_raises():
    with pytest.raises(ValueError):
        to_unit(1000, "XB")


def test_constants_match_units():
    assert KB == 1000
    assert MIB == 1024 ** 2
    assert GB == 1000 ** 3


def test_constants_used_for_arithmetic():
    assert humanize(5 * MB) == "5.0 MB"


def test_total_mixed_int_and_strings():
    # parse() uses SI semantics for "KB"/"MB" (1000-based) and binary for "KiB"/"MiB".
    assert total(1024, "1KB", "2MB") == 1024 + 1000 + 2_000_000


def test_total_empty():
    assert total() == 0


def test_total_single_int():
    assert total(100) == 100


def test_total_binary_units():
    assert total("1 KiB", "1 MiB") == 1024 + 1024**2


def test_total_rejects_other_types():
    with pytest.raises(TypeError):
        total(1.5)  # type: ignore[arg-type]


def test_compare_less():
    assert compare(100, 200) == -1


def test_compare_greater():
    assert compare(200, 100) == 1


def test_compare_equal():
    assert compare(100, 100) == 0


def test_compare_string_vs_int_si():
    # parse("1 KB") == 1000, so "1 KB" < 1024.
    assert compare("1 KB", 1024) == -1


def test_compare_string_vs_int_equal():
    assert compare("1 KiB", 1024) == 0


def test_compare_two_strings():
    assert compare("1 MB", "1 KB") == 1


def test_from_unit_kb():
    assert from_unit(1.5, "KB") == 1500


def test_from_unit_mib():
    assert from_unit(2, "MiB") == 2 * 1024 ** 2


def test_from_unit_case_insensitive():
    assert from_unit(1, "kb") == from_unit(1, "KB")


def test_from_unit_unknown_raises():
    with pytest.raises(ValueError):
        from_unit(1, "XB")


def test_from_unit_round_trip_with_to_unit():
    bytes_value = from_unit(1.5, "MB")
    assert to_unit(bytes_value, "MB") == 1.5

