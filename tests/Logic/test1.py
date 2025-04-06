import pytest
from unittest.mock import patch
from typing import List

from jsons.exceptions import JsonsError, DeserializationError

from jsons.deserializers.default_list import default_list_deserializer

def test_with_generic_type():
    result = default_list_deserializer(
        ["1", "2", "3"],
        cls=list[int], 
        tasks=1
    )
    assert result == [1, 2, 3]  
def test_without_generic_type():
    result = default_list_deserializer(
        [1, 2, 3],
        cls=None,  
        tasks=1
    )
    assert result == [1, 2, 3]

def test_single_task():
    with patch("jsons._load_impl.load", side_effect=lambda x, **kwargs: x):
        result = default_list_deserializer(
            [1, 2, 3],
            cls=list[int],
            tasks=1 
        )
        assert result == [1, 2, 3]

def test_multi_task():
    with patch("jsons._multitasking.multi_task", return_value=[1, 2, 3]):
        result = default_list_deserializer(
            [1, 2, 3],
            cls=list[int],
            tasks=2  
        )
        assert result == [1, 2, 3]

def test_invalid_tasks():
    with pytest.raises(JsonsError, match="Invalid number of tasks"):
        default_list_deserializer(
            [1, 2, 3],
            cls=list[int],
            tasks=0 
        )

def test_warn_on_fail():
    def mock_load(elem, **kwargs):
        if elem == "fail":
            raise DeserializationError("Failed", source=elem, target=int)
        return elem

    with patch("jsons._load_impl.load", side_effect=mock_load):
        with pytest.warns(UserWarning, match="Could not deserialize element at index 1"):
            result = default_list_deserializer(
                [1, "fail", 3],
                cls=list[int],
                warn_on_fail=True
            )
        assert result == [1, 3]  

def test_raise_on_fail():
    def mock_load(elem, **kwargs):
        if elem == "fail":
            raise DeserializationError("Failed", source=elem, target=int)
        return elem

    with patch("jsons._load_impl.load", side_effect=mock_load):
        with pytest.raises(DeserializationError) as exc_info:
            default_list_deserializer(
                [1, "fail", 3],  
                cls=List[int],
                warn_on_fail=False
            )