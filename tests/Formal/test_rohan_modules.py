# tests/Formal/test_rohan_modules.py

import pytest
from jsons.deserializers.default_complex import default_complex_deserializer
from jsons._datetime_impl import to_str
from datetime import timezone, timedelta, datetime, tzinfo
from jsons.exceptions import DeserializationError


def test_default_complex_valid():
    """Test default_complex_deserializer with valid complex input."""
    data = {"real": 2.0, "imag": -3.5}
    result = default_complex_deserializer(data)
    assert result == complex(2.0, -3.5)


def test_default_complex_missing_real_key():
    """Test default_complex_deserializer with missing 'real' key."""
    data = {"imag": 4.0}
    with pytest.raises(AttributeError) as exc_info:
        default_complex_deserializer(data)
    assert "does not contain key 'real'" in str(exc_info.value)


def test_default_complex_type_error():
    """Test default_complex_deserializer with invalid float casting."""
    data = {"real": "a", "imag": 2.0}
    with pytest.raises(AttributeError) as exc_info:
        default_complex_deserializer(data)
    assert "cannot cast value" in str(exc_info.value)


def test_to_str_basic_utc():
    """Test to_str function with UTC datetime."""
    dt = datetime(2025, 4, 1, 15, 30, tzinfo=timezone.utc)
    result = to_str(dt, strip_microseconds=True, fork_inst=type("Mock", (), {"_warn": lambda *args, **kwargs: None}))
    assert result.endswith("+00:00") or result.endswith("Z")


def test_to_str_strip_microseconds_false():
    """Test to_str with microseconds included."""
    dt = datetime(2025, 4, 1, 15, 30, 45, 123456, tzinfo=timezone.utc)
    result = to_str(dt, strip_microseconds=False, fork_inst=type("Mock", (), {"_warn": lambda *args, **kwargs: None}))
    assert ".123456" in result


def test_to_str_with_offset():
    """Test to_str with a positive UTC offset."""
    class CustomTZ(tzinfo):
        def utcoffset(self, dt):
            return timedelta(hours=5, minutes=30)
        def tzname(self, dt):
            return "CustomTZ"
        def dst(self, dt):
            return timedelta(0)

    dt = datetime(2025, 4, 1, 12, 0, tzinfo=CustomTZ())
    result = to_str(dt, strip_microseconds=True, fork_inst=type("Mock", (), {"_warn": lambda *args, **kwargs: None}))
    assert result.endswith("+05:30")


def test_to_str_warns_on_missing_timezone():
    """Test that a warning is issued if timezone is missing."""
    class WarnCapture:
        called = False
        @staticmethod
        def _warn(msg, code):
            WarnCapture.called = True

    dt = datetime(2025, 4, 1, 12, 0)  # no tzinfo
    result = to_str(dt, strip_microseconds=True, fork_inst=WarnCapture)
    assert WarnCapture.called
    assert result.endswith("+00:00") or "+" in result or "Z" in result
