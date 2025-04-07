import pytest
from jsons._validation import set_validator, validate, ValidationError

# Simple validator for age
def age_validator(age):
    if not isinstance(age, int):
        raise ValueError("Age must be an integer")
    if not (0 <= age <= 120):
        raise ValueError("Invalid age")
    return True

# Register validator once for int
set_validator(age_validator, int)

def test_age_below_minimum():
    with pytest.raises(ValidationError):
        validate(-1, int)

def test_age_minimum_valid():
    validate(0, int)  # Should not raise

def test_age_just_above_min():
    validate(1, int)  # Should not raise

def test_age_maximum_valid():
    validate(120, int)  # Should not raise

def test_age_above_maximum():
    with pytest.raises(ValidationError):
        validate(121, int)

def test_age_wrong_type_string():
    with pytest.raises(ValidationError):
        validate("50", int)

def test_age_sequence_registration():
    # Register same validator for list of types
    def dummy_validator(x): return True
    set_validator(dummy_validator, [str, float])
    validate("hello", str)
    validate(3.14, float)
