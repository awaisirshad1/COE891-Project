import unittest
from jsons._load_impl import load, loads, loadb
from dataclasses import dataclass
import json

@dataclass
class Person:
    name: str
    age: int

class TestLoadImplBVA(unittest.TestCase):

    def test_load_empty_dict(self):
        with self.assertRaises(Exception):
            load({}, Person)

    def test_load_minimum_valid(self):
        result = load({'name': 'A', 'age': 0}, Person)
        self.assertEqual(result.age, 0)

    def test_load_maximum_valid(self):
        result = load({'name': 'Zoe', 'age': 120}, Person)
        self.assertEqual(result.age, 120)

    def test_load_none_value(self):
        with self.assertRaises(Exception):
            load(None, Person)

    def test_loads_invalid_json(self):
        with self.assertRaises(Exception):
            loads("{invalid", Person)

    def test_loads_large_json(self):
        json_str = json.dumps({'name': 'John', 'age': 99})
        result = loads(json_str, Person)
        self.assertEqual(result.name, 'John')

    def test_loadb_utf8(self):
        result = loadb(b'{"name": "Alice", "age": 25}', Person)
        self.assertEqual(result.age, 25)

    def test_loadb_ascii_failure(self):
        with self.assertRaises(UnicodeDecodeError):
            loadb("Üser".encode('utf-8'), Person, encoding='ascii')