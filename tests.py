from src.pyson_data import (
    Type,
    Value,
    is_valid_pyson,
    is_valid_pyson_entry,
)
import unittest


class PysonTests(unittest.TestCase):

    def test_pyson(self):
        print("Starting PYSON tests...\n")
        self.assertTrue(all([t == Type(t).__str__() for t in ["int", "float", "str", "list"]]))

        examples = (
            (str(Type(t)), Value(v).type_str())
            for t, v in
            [("str", "string"), ("int", 123), ("float", 3.14), ("list", ["list", "of", "strings"])]
        )
        for t, v in examples:
            self.assertEqual(t, v)
        with open("tests/example.pyson") as f:
            lines = f.read().split("\n")
        for line in lines:
            self.assertTrue(line == "" or is_valid_pyson_entry(line), f"Invalid pyson entry: {line}")
            self.assertTrue(is_valid_pyson(line), f"Invalid pyson: \"{line}\"")

        print("All tests passed!")
