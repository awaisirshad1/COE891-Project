import pytest
from datetime import datetime, date, timedelta, timezone
from jsons._datetime_impl import to_str, get_datetime_inst, _timedelta_offset_str

class DummyFork:
    @staticmethod
    def _warn(msg, code): pass

def test_to_str_min_datetime():
    dt = datetime.min.replace(tzinfo=timezone.utc)
    result = to_str(dt, strip_microseconds=True, fork_inst=DummyFork)
    assert result.startswith("0001-01-01T")

def test_to_str_max_microseconds():
    dt = datetime(2024, 1, 1, 23, 59, 59, 999999, tzinfo=timezone.utc)
    result = to_str(dt, strip_microseconds=False, fork_inst=DummyFork)
    assert "." in result 
    assert result.endswith('Z') or result.endswith('+00:00')

def test_to_str_no_microseconds():
    dt = datetime(2024, 1, 1, 12, 0, 0, 0, tzinfo=timezone.utc)
    result = to_str(dt, strip_microseconds=True, fork_inst=DummyFork)
    assert "." not in result

def test_get_datetime_inst_min_date():
    dt_str = "0001-01-01T00:00:00Z"
    result = get_datetime_inst(dt_str, "%Y-%m-%dT%H:%M:%S")
    assert result.year == 1 and result.tzinfo is not None

def test_get_datetime_inst_max_date():
    dt_str = "9999-12-31T23:59:59Z"
    result = get_datetime_inst(dt_str, "%Y-%m-%dT%H:%M:%S")
    assert result.year == 9999

def test_get_datetime_inst_invalid_format():
    with pytest.raises(ValueError):
        get_datetime_inst("2023-12-01 12:00:00", "%Y-%m-%dT%H:%M:%S")

def test_timedelta_offset_zero():
    td = timedelta()
    result = _timedelta_offset_str(td)
    assert result == "+00:00" or result == "-00:00"

def test_timedelta_offset_max():
    td = timedelta(hours=14)
    result = _timedelta_offset_str(td)
    assert result == "+14:00"

def test_timedelta_offset_negative():
    td = timedelta(hours=-12)
    result = _timedelta_offset_str(td)
    assert result == "-12:00"
