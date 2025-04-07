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