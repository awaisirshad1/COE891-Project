import pytest
from collections import defaultdict
from typing import DefaultDict
from jsons.deserializers.default_defaultdict import default_defaultdict_deserializer  # Replace with your module name

def test_non_parameterized_defaultdict():
    obj = {"a": 1, "b": 2}
    result = default_defaultdict_deserializer(obj, defaultdict)

    assert isinstance(result, defaultdict)
    assert result.default_factory is None  
    assert dict(result) == obj

    with pytest.raises(KeyError):
        _ = result["missing_key"]

def test_parameterized_defaultdict():
    cls = DefaultDict[str, int]
    obj = {"a": "1", "b": "2"} 

    result = default_defaultdict_deserializer(
        obj,
        cls,
        key_transformer=lambda x: x, 
    )

    assert isinstance(result, defaultdict)
    assert result.default_factory is int 

    assert dict(result) == {"a": 1, "b": 2}

    assert result["missing_key"] == 0 

def test_invalid_defaultdict_args():
    class InvalidDefaultDict(defaultdict):
        __args__ = (str,)  

    obj = {"a": 1}
    with pytest.raises(ValueError):
        default_defaultdict_deserializer(obj, InvalidDefaultDict)