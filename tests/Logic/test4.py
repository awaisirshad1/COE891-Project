from typing import Tuple, Optional
from collections import namedtuple

from jsons.deserializers.default_tuple import default_tuple_deserializer
from jsons.deserializers.default_tuple import default_namedtuple_deserializer

Point = namedtuple('Point', ['x', 'y'], defaults=[0])
Point.__annotations__ = {'x': int, 'y': int}

def test_tuple_deserializer_named_tuple():
    result = default_tuple_deserializer([1, 2], Point)
    assert result == Point(1, 2)

def test_tuple_deserializer_specific_types():
    result = default_tuple_deserializer(["1", "two"], Tuple[int, str])
    assert result == (1, "two")

def test_tuple_deserializer_ellipsis():
    result = default_tuple_deserializer(["1", "2", "3"], Tuple[int, ...])
    assert result == (1, 2, 3)

def test_tuple_deserializer_no_specific_types():
    result = default_tuple_deserializer([1, "two"], tuple)
    assert result == (1, "two")

def test_named_tuple_with_default():
    result = default_tuple_deserializer([1], Point)
    assert result == Point(1, 0)

def test_tuple_ellipsis_different_lengths():
    result = default_tuple_deserializer(["1"], Tuple[int, ...])
    assert result == (1,)
    result = default_tuple_deserializer(["1", "2"], Tuple[int, ...])
    assert result == (1, 2)

def test_tuple_no_types_any_input():
    result = default_tuple_deserializer([1, "string", 3.14], tuple)
    assert result == (1, "string", 3.14)

def test_namedtuple_deserializer_list_input():
    result = default_namedtuple_deserializer([1, 2], Point)
    assert result == Point(1, 2)

def test_namedtuple_deserializer_dict_input():
    result = default_namedtuple_deserializer({"x": 1, "y": 2}, Point)
    assert result == Point(1, 2)

def test_namedtuple_deserializer_missing_field_with_default():
    result = default_namedtuple_deserializer([1], Point)
    assert result == Point(1, 0)

def test_namedtuple_deserializer_none_allowed():
    PointWithOptional = namedtuple('PointWithOptional', ['x'], defaults=[None])
    PointWithOptional.__annotations__ = {'x': Optional[int]}
    result = default_namedtuple_deserializer([None], PointWithOptional)
    assert result == PointWithOptional(None)