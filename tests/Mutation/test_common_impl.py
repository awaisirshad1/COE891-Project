import pytest
import builtins
import warnings
from typing import List, Dict, Union, Optional, Any
from unittest import TestCase, mock
from jsons._common_impl import (
    get_class_name,
    get_cls_from_str,
    determine_precedence,
    get_cls_and_meta,
    can_match_with_none,
    _get_simple_name,
    _get_module,
    _get_generic_cls_from_str,
    _lookup_announced_class,
    StateHolder,
    META_ATTR,
    NoneType
)


class TestCommonImpl(TestCase):
    def setUp(self):
        self.state = StateHolder()
        self.state._announced_classes = {}

    # Expanded get_class_name tests
    def test_get_class_name_without__name__(self):
        class Meta(type):
            __name__ = None

        class C(metaclass=Meta):
            pass

        self.assertEqual('C', get_class_name(C))
        self.assertEqual(f'{__name__}.C',
                         get_class_name(C, fully_qualified=True))

    def test_get_class_name_with_transformer(self):
        self.assertEqual('str', get_class_name(str, transformer=str.lower))
        self.assertEqual('STR', get_class_name(str, transformer=str.upper))

    def test_get_class_name_of_none(self):
        self.assertEqual('NoneType', get_class_name(None))
        self.assertEqual('nonetype', get_class_name(None, transformer=str.lower))

    def test_get_class_name_special_cases(self):
        from typing import NewType
        UserId = NewType('UserId', int)
        self.assertEqual('UserId', get_class_name(UserId))

    # Expanded get_cls_from_str tests
    def test_get_cls_from_str_builtin(self):
        self.assertEqual(str, get_cls_from_str('str', {}, self.state))
        self.assertEqual(int, get_cls_from_str('int', {}, self.state))
        self.assertEqual(list, get_cls_from_str('list', {}, self.state))
        self.assertEqual(dict, get_cls_from_str('dict', {}, self.state))


    def test_get_cls_from_str_announced_class(self):
        class TestClass: pass

        self.state._announced_classes['TestClass'] = TestClass
        self.assertEqual(TestClass, get_cls_from_str('TestClass', {}, self.state))

    # Test determine_precedence
    def test_determine_precedence_basic(self):
        class A: pass

        class B: pass

        class C: pass

        result = determine_precedence(A, B, C, False)
        self.assertEqual(A, result)

        result = determine_precedence(None, B, C, False)
        self.assertEqual(B, result)

        result = determine_precedence(None, None, C, False)
        self.assertEqual(C, result)

    def test_determine_precedence_inferred(self):
        class A: pass

        class B: pass

        class C: pass

        result = determine_precedence(A, B, C, True)
        self.assertEqual(B, result)

    # Test get_cls_and_meta
    def test_get_cls_and_meta_with_meta(self):
        json_obj = {
            META_ATTR: {
                'classes': {'/': 'str'},
                'other_meta': 'data'
            }
        }
        cls, meta = get_cls_and_meta(json_obj, self.state)
        self.assertEqual(str, cls)
        self.assertEqual(json_obj[META_ATTR], meta)

    def test_get_cls_and_meta_without_meta(self):
        json_obj = {'key': 'value'}
        cls, meta = get_cls_and_meta(json_obj, self.state)
        self.assertIsNone(cls)
        self.assertIsNone(meta)

    # Test can_match_with_none
    def test_can_match_with_none_basic_types(self):
        self.assertTrue(can_match_with_none(Any))
        self.assertTrue(can_match_with_none(object))
        self.assertTrue(can_match_with_none(None))
        self.assertTrue(can_match_with_none(NoneType))
        self.assertFalse(can_match_with_none(str))
        self.assertFalse(can_match_with_none(int))

    def test_can_match_with_none_union_types(self):
        self.assertTrue(can_match_with_none(Optional[str]))
        self.assertTrue(can_match_with_none(Union[str, None]))
        self.assertTrue(can_match_with_none(Union[str, int, None]))
        self.assertFalse(can_match_with_none(Union[str, int]))

    # Test _get_simple_name
    def test_get_simple_name_with_name(self):
        self.assertEqual('str', _get_simple_name(str))

    def test_get_simple_name_without_name(self):
        class C:
            __name__ = None

        self.assertEqual('C', _get_simple_name(C))

    # Test _get_module
    def test_get_module_builtin(self):
        self.assertIsNone(_get_module(str))

    def test_get_module_custom_class(self):
        class TestClass: pass

        self.assertEqual(__name__, _get_module(TestClass))

    # Test StateHolder warnings
    def test_state_holder_warnings(self):
        with warnings.catch_warnings(record=True) as w:
            StateHolder._warn("Test warning", "test_code")
            self.assertEqual(1, len(w))
            self.assertIn("Test warning", str(w[0].message))

    def test_state_holder_suppressed_warnings(self):
        StateHolder._suppressed_warnings.add("suppressed_code")
        with warnings.catch_warnings(record=True) as w:
            StateHolder._warn("Should not appear", "suppressed_code")
            self.assertEqual(0, len(w))
        StateHolder._suppressed_warnings.remove("suppressed_code")