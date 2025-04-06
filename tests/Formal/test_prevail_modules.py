# tests/Formal/test_prevail_modules.py

import pytest
from jsons.deserializers import default_list, default_date, default_dict, default_enum, default_string
from datetime import date
from enum import Enum
from typing import List, Dict


def test_default_list_deserializer_with_ints():
    """Test that default_list_deserializer properly deserializes a list of integers."""
    data = ['1', '2', '3']
    result = default_list.default_list_deserializer(data, List[int])
    assert result == [1, 2, 3]


def test_default_list_deserializer_warn_on_fail():
    """Test that default_list_deserializer skips invalid elements with warn_on_fail=True."""
    data = ['1', 'two', '3']
    result = default_list.default_list_deserializer(data, List[int], warn_on_fail=True)
    assert result == [1, 3]  # Skips the invalid 'two'


def test_default_date_deserializer_rfc3339():
    """Test that default_date_deserializer correctly parses RFC3339 formatted date string."""
    data = '2023-10-12'
    result = default_date.default_date_deserializer(data)
    assert result == date(2023, 10, 12)


def test_default_dict_deserializer_basic():
    """Test that default_dict_deserializer deserializes a dict with string keys and int values."""
    data = {'a': '1', 'b': '2'}
    result = default_dict.default_dict_deserializer(data, Dict[str, int])
    assert result == {'a': 1, 'b': 2}


def test_default_dict_deserializer_with_key_transform():
    """Test that default_dict_deserializer uses a key transformer function during deserialization."""
    data = {'FirstName': 'John', 'LastName': 'Doe'}
    transformer = lambda k: k.lower()
    result = default_dict.default_dict_deserializer(data, Dict[str, str], key_transformer=transformer)
    assert result == {'firstname': 'John', 'lastname': 'Doe'}


def test_default_enum_deserializer_by_name():
    """Test that default_enum_deserializer deserializes enum by name when use_enum_name=True."""
    class Color(Enum):
        RED = 1
        BLUE = 2
    result = default_enum.default_enum_deserializer('RED', Color, use_enum_name=True)
    assert result == Color.RED


def test_default_enum_deserializer_by_value():
    """Test that default_enum_deserializer deserializes enum by value when use_enum_name=False."""
    class Color(Enum):
        RED = 1
        BLUE = 2
    result = default_enum.default_enum_deserializer(1, Color, use_enum_name=False)
    assert result == Color.RED


def test_default_string_deserializer_to_str():
    """Test that default_string_deserializer returns the original string when target type is str."""
    result = default_string.default_string_deserializer("hello", str)
    assert result == "hello"


def test_default_string_deserializer_to_datetime_fallback():
    """Test that default_string_deserializer falls back to string if datetime parse fails."""
    result = default_string.default_string_deserializer("not-a-date", str)
    assert result == "not-a-date"
