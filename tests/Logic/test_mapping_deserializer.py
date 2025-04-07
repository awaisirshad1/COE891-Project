from collections.abc import Mapping
from typing import Mapping as MappingType
from jsons.deserializers.default_mapping import default_mapping_deserializer  # Replace with actual import

def test_non_generic_mapping():
    obj = {"a": 1, "b": 2}
    result = default_mapping_deserializer(obj, Mapping)
    assert isinstance(result, dict) 
    assert result == obj

def test_generic_mapping():
    obj = {"a": "1", "b": "2"}
    cls = MappingType[str, int]  
    result = default_mapping_deserializer(obj, cls)
    assert isinstance(result, dict)
    assert result == {"a": 1, "b": 2}  
