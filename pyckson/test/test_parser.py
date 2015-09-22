from unittest import TestCase
from pyckson.parser import parse
from pyckson.decorators import pyckson, listtype


class ParserTest(TestCase):
    def test_simple_class(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        result = parse(Foo, {'bar': 'bar'})

        self.assertEqual(result.bar, 'bar')

    def test_class_with_list(self):
        @pyckson
        @listtype('bar', str)
        class Foo:
            def __init__(self, bar: list):
                self.bar = bar

        result = parse(Foo, {'bar': ['a', 'b']})

        self.assertListEqual(result.bar, ['a', 'b'])

    def test_class_with_optional_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, a: int, b: str=None):
                self.a = a
                self.b = b

        result = parse(Foo, {'a': 42})

        self.assertEqual(result.a, 42)
        self.assertIsNone(result.b)

    def test_class_with_missing_attribute(self):
        @pyckson
        class Foo:
            def __init__(self, bar: str):
                self.bar = bar

        with self.assertRaises(ValueError):
            parse(Foo, {})
