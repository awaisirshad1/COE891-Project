import pytest
from jsons._transform_impl import transform
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

# --- BVA TEST CASES ---

def test_transform_minimal_valid():
    input_data = {"name": "Alice", "age": 0}
    person = transform(input_data, Person)
    assert person.age == 0
    assert person.name == "Alice"

def test_transform_maximum_valid():
    input_data = {"name": "Zoe", "age": 120}
    person = transform(input_data, Person)
    assert person.age == 120

def test_transform_above_max_age():
    input_data = {"name": "Bob", "age": 150}
    person = transform(input_data, Person)
    assert person.age == 150  # No validation set, so it will still pass

# supposed to Fail because 'age' field is missing → raises UnfulfilledArgumentError
def test_transform_missing_field():
    input_data = {"name": "NoAge"}
    with pytest.raises(TypeError):  # Missing required field
        transform(input_data, Person)

def test_transform_extra_field():
    input_data = {"name": "Alice", "age": 25, "location": "Canada"}
    person = transform(input_data, Person)
    assert person.name == "Alice" and person.age == 25

# Fails because mapper removes 'age' → required field missing → UnfulfilledArgumentError
def test_transform_mapper_drops_required_field():
    input_data = {"name": "Alice", "age": 25}

    def drop_age(data):
        data.pop("age")
        return data

    with pytest.raises(TypeError):  # Missing required field after mapping
        transform(input_data, Person, mapper=drop_age)

def test_transform_mapper_modifies_field_type():
    input_data = {"name": "Alice", "age": 25}

    def make_age_string(data):
        data["age"] = "twenty-five"
        return data

    with pytest.raises(Exception):  # Type mismatch for age (expects int)
        transform(input_data, Person, mapper=make_age_string)

# Fails because input is empty dict → required fields 'name' and 'age' missing → UnfulfilledArgumentError
def test_transform_empty_dict():
    with pytest.raises(TypeError):
        transform({}, Person)

# Fails because 'strict=True' rejects extra 'extra' field → raises SignatureMismatchError
def test_transform_with_strict_kwarg():
    input_data = {"name": "Alice", "age": 25, "extra": "data"}
    person = transform(input_data, Person, strict=True)
    assert person.name == "Alice"
