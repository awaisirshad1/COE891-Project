from typing import Tuple, Optional
from collections import namedtuple

from jsons.deserializers.default_tuple import default_tuple_deserializer
from jsons.deserializers.default_tuple import default_namedtuple_deserializer

Point = namedtuple('Point', ['x', 'y'], defaults=[0])
Point.__annotations__ = {'x': int, 'y': int}


def test_tuple_deserializer_ellipsis():
    result = default_tuple_deserializer(["1", "2", "3"], Tuple[int, ...])
    assert result == (1, 2, 3)

def test_tuple_deserializer_no_specific_types():
    result = default_tuple_deserializer([1, "two"], tuple)
    assert result == (1, "two")
