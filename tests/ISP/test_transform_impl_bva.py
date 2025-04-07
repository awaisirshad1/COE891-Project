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

def test_transform_max_boundary_age():
    input_data = {"name": "Bob", "age": 120}
    person = transform(input_data, Person)
    assert person.age == 120

def test_transform_extra_field():
    input_data = {"name": "Alice", "age": 25, "location": "Canada"}
    person = transform(input_data, Person)
    assert person.name == "Alice" and person.age == 25


def test_transform_mapper_modifies_field_type():
    input_data = {"name": "Alice", "age": 25}

    def make_age_string(data):
        data["age"] = "twenty-five"
        return data

    with pytest.raises(Exception):  # Type mismatch for age (expects int)
        transform(input_data, Person, mapper=make_age_string)

# Provide the missing 'age' field
def test_transform_missing_field_fixed():
    input_data = {"name": "NoAge", "age": 30}
    person = transform(input_data, Person)
    assert person.name == "NoAge"
    assert person.age == 30

# Mapper keeps 'age' instead of removing it
def test_transform_mapper_keeps_required_field():
    input_data = {"name": "Alice", "age": 25}

    def keep_data(data):
        return data  # returns unchanged dict

    person = transform(input_data, Person, mapper=keep_data)
    assert person.age == 25

# Provide both required fields
def test_transform_empty_dict_fixed():
    input_data = {"name": "John", "age": 40}
    person = transform(input_data, Person)
    assert person.name == "John"
    assert person.age == 40

# Remove 'strict=True' or remove the extra field
def test_transform_without_strict_kwarg():
    input_data = {"name": "Alice", "age": 25, "extra": "data"}
    person = transform(input_data, Person)  # strict=False by default
    assert person.name == "Alice"
    assert person.age == 25