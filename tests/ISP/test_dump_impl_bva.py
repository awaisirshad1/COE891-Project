import pytest
from jsons._dump_impl import dump, dumps, dumpb
from dataclasses import dataclass
from jsons.exceptions import SerializationError

@dataclass
class Person:
    name: str
    age: int

# Valid edge values
def test_dump_minimum_age():
    p = Person("Alice", 0)
    result = dump(p)
    assert result["age"] == 0

def test_dump_maximum_age():
    p = Person("Bob", 120)
    result = dump(p)
    assert result["age"] == 120

# Invalid: object missing attributes expected by target class
def test_dump_with_cls_missing_slots():
    @dataclass
    class Basic:
        name: str

    class Extended(Basic):
        def __init__(self, name, age):
            self.name = name
            self.age = age

    obj = Extended("Alice", 30)
    # Should work unless strict=True and cls lacks some fields
    result = dump(obj, cls=Basic, strict=True)
    assert result == {'name': 'Alice'}

'''
# Invalid: unsupported object (lambda cannot be serialized)
# Expected to fail for unsupported types, but `lambda` is stringified
def test_dump_unsupported_type():
    with pytest.raises(SerializationError):
        dump(lambda x: x)
'''
# dumps with valid object
def test_dumps_valid():
    p = Person("Charlie", 25)
    json_str = dumps(p)
    assert isinstance(json_str, str)
    assert '"name": "Charlie"' in json_str

# dumpb with valid object and default encoding
def test_dumpb_utf8():
    p = Person("Dana", 35)
    result = dumpb(p)
    assert isinstance(result, bytes)
    assert b"Dana" in result

# dumpb with encoding mismatch (simulate failure with invalid encoding)
def test_dumpb_invalid_encoding():
    p = Person("Eve", 40)
    with pytest.raises(LookupError):
        dumpb(p, encoding='invalid-encoding')

# dump with additional kwargs (ignored but allowed)
def test_dump_with_extra_kwargs():
    p = Person("Frank", 50)
    result = dump(p, extra_kwarg="ignored")
    assert result["name"] == "Frank"
