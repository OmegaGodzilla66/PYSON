from pyson_data import (
    Type,
    Value,
    is_valid_pyson,
    is_valid_pyson_entry,
)

assert all([t == Type(t).__str__() for t in ["int", "float", "str", "list"]])

examples = (
    (str(Type(t)), Value(v).type_str())
    for t, v in
    [("str", "string"), ("int", 123), ("float", 3.14), ("list", ["list", "of", "strings"])]
)
for t, v in examples:
    assert t == v

lines = open("example.pyson").read().split("\n")
for line in lines:
    assert line == "" or is_valid_pyson_entry(line), f"Invalid pyson entry: {line}"
    assert is_valid_pyson(line), f"Invalid pyson: \"{line}\""

print("All tests passed!")