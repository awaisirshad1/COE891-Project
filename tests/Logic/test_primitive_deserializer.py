import pytest
from jsons.exceptions import DeserializationError
from jsons.deserializers.default_primitive import default_primitive_deserializer  

def test_none_input():
    assert default_primitive_deserializer(None, int) is None 

def test_no_conversion_needed():
    assert default_primitive_deserializer(42, int) == 42  
    assert default_primitive_deserializer("hello", str) == "hello"
