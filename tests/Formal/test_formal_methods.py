# tests/Formal/test_formal_methods.py

import pytest
import jsons
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

def test_primitive_reversibility():
    """Test that primitive types are reversible through serialization and deserialization."""
    primitives = [42, 3.14, True, "hello", None]
    for item in primitives:
        dumped = jsons.dumps(item)
        loaded = jsons.loads(dumped, type(item))
        assert item == loaded

def test_complex_object_reversibility():
    """Test that complex objects are reversible through serialization and deserialization."""
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    person = Person("Alice", 30)
    dumped = jsons.dumps(person)
    loaded = jsons.loads(dumped, Person)
    assert person == loaded

def test_nested_structure_reversibility():
    """Test that nested structures are reversible through serialization and deserialization."""
    data = {"numbers": [1, 2, 3], "info": {"name": "Bob", "age": 25}}
    dumped = jsons.dumps(data)
    loaded = jsons.loads(dumped, dict)
    assert data == loaded

def test_datetime_serialization():
    """Test that datetime objects are correctly serialized and deserialized."""
    now = datetime.now(timezone.utc)  # Make timezone-aware
    dumped = jsons.dumps(now)
    loaded = jsons.loads(dumped, datetime)
    assert now == loaded

def test_decimal_serialization():
    """Test that Decimal objects are correctly serialized and deserialized."""
    value = Decimal("10.5")
    dumped = jsons.dumps(value)
    loaded = jsons.loads(dumped, Decimal)
    assert value == loaded

def test_uuid_serialization():
    """Test that UUID objects are correctly serialized and deserialized."""
    value = UUID("12345678123456781234567812345678")
    dumped = jsons.dumps(value)
    loaded = jsons.loads(dumped, UUID)
    assert value == loaded

def test_idempotent_serialization():
    """Test that serializing and deserializing repeatedly returns same result."""
    data = {"key": "value"}
    dumped_once = jsons.dumps(data)
    dumped_twice = jsons.dumps(jsons.loads(dumped_once))
    assert dumped_once == dumped_twice

def test_type_preservation():
    """Test that the type of the object is preserved after serialization and deserialization."""
    data = {"count": 10, "rate": 3.5, "active": True, "name": "Test"}
    dumped = jsons.dumps(data)
    loaded = jsons.loads(dumped, dict)
    assert isinstance(loaded["count"], int)
    assert isinstance(loaded["rate"], float)
    assert isinstance(loaded["active"], bool)
    assert isinstance(loaded["name"], str)

def test_error_handling_unsupported_type():
    """Test that serializing an unsupported type raises a JsonsError."""
    f = open(__file__)  # File objects are not serializable
    with pytest.raises(jsons.exceptions.JsonsError):
        jsons.dumps(f)

def test_error_handling_malformed_json():
    """Test that deserializing malformed JSON raises a JsonsError."""
    malformed_json = '{"name": "Alice", "age": 30'  # Missing closing brace
    with pytest.raises(jsons.JsonsError):
        jsons.loads(malformed_json, dict)
