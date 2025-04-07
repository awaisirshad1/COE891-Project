from datetime import datetime
from jsons._datetime_impl import RFC3339_DATETIME_PATTERN
from jsons.deserializers.default_datetime import default_datetime_deserializer  # Replace with actual import

def _convert_rfc3339_to_strptime_format(dt_str: str) -> str:
    """Helper to convert RFC3339 'Z' to '+0000' for strptime parsing."""
    if dt_str.endswith('Z'):
        return dt_str.replace('Z', '+0000')
    return dt_str

def test_datetime_with_fractional_seconds():
    obj = "2023-10-01T12:34:56.123456Z"
    result = default_datetime_deserializer(obj)
    assert isinstance(result, datetime)

    expected = datetime.strptime(
        _convert_rfc3339_to_strptime_format(obj),
        RFC3339_DATETIME_PATTERN + ".%f%z"
    )
    assert result == expected 


def test_datetime_without_fractional_seconds():
    obj = "2023-10-01T12:34:56Z"
    result = default_datetime_deserializer(obj)
    assert isinstance(result, datetime)

    expected = datetime.strptime(
        _convert_rfc3339_to_strptime_format(obj),
        RFC3339_DATETIME_PATTERN + "%z"
    )
    assert result == expected  