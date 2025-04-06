from jsons.deserializers.default_enum import default_enum_deserializer
from enum import Enum

class Color(Enum):
    RED = 1
    BLUE = 2

def test_use_enum_name_true():
    result = default_enum_deserializer("RED", Color, use_enum_name=True)
    assert result == Color.RED

def test_use_enum_name_false():
    result = default_enum_deserializer(1, Color, use_enum_name=False)
    assert result == Color.RED

def test_use_enum_none_name_success():
    result = default_enum_deserializer("RED", Color, use_enum_name=None)
    assert result == Color.RED

def test_use_enum_none_value_success():
    result = default_enum_deserializer(1, Color, use_enum_name=None)
    assert result == Color.RED



def test_clause_use_enum_name_true_valid():
    result = default_enum_deserializer("BLUE", Color, use_enum_name=True)
    assert result == Color.BLUE

def test_clause_use_enum_name_true_invalid():
    try:
        default_enum_deserializer("GREEN", Color, use_enum_name=True)
        assert False, "Should have raised KeyError"
    except KeyError:
        assert True

def test_clause_use_enum_name_false_valid():
    result = default_enum_deserializer(2, Color, use_enum_name=False)
    assert result == Color.BLUE

def test_clause_use_enum_name_false_invalid():
    try:
        default_enum_deserializer(3, Color, use_enum_name=False)
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True

def test_clause_use_enum_none_name():
    result = default_enum_deserializer("RED", Color, use_enum_name=None)
    assert result == Color.RED

def test_clause_use_enum_none_value():
    result = default_enum_deserializer(1, Color, use_enum_name=None)
    assert result == Color.RED

def test_clause_use_enum_none_invalid():
    try:
        default_enum_deserializer("GREEN", Color, use_enum_name=None)
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True
