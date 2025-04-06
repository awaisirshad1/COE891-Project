from typing import Dict
from jsons.deserializers.default_dict import _load_hashed_keys, _deserialize

# --- Tests for _load_hashed_keys ---
def test_load_hashed_keys_with_stored_keys():
    obj = {"-keys": {"k1": "original"}, "k1": "value"}
    cls = Dict[str, str]
    result, keys_were_hashed = _load_hashed_keys(obj, cls, (str, str))
    assert result == {"original": "value"}
    assert keys_were_hashed is True

def test_load_hashed_keys_without_stored_keys():
    obj = {"key": "value"}
    cls = Dict[str, str]
    result, keys_were_hashed = _load_hashed_keys(obj, cls, (str, str))
    assert result == obj
    assert keys_were_hashed is False

# --- Tests for _deserialize ---
def test_deserialize_with_cls_args_and_unhashed_keys():
    obj = {"key": "1"}
    result = _deserialize(obj, (str, int), None, False, {})
    assert result == {"key": 1} 

def test_deserialize_with_cls_args_and_hashed_keys():
    obj = {"key": "1"}
    result = _deserialize(obj, (str, int), None, True, {})
    assert result == {"key": 1}  
def test_deserialize_without_cls_args():
    obj = {"key": "1"}
    result = _deserialize(obj, (), None, False, {})
    assert result == {"key": "1"}