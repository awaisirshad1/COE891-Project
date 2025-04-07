import pytest
from jsons.exceptions import DeserializationError
from jsons.deserializers.default_nonetype import default_nonetype_deserializer  # Replace with actual import

def test_none_input():
    assert default_nonetype_deserializer(None) is None  # Passes

def test_non_none_input():
    with pytest.raises(DeserializationError):
        default_nonetype_deserializer("not None")  # Raises error
