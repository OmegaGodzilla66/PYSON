import os
import pyson_data as pyson

# this is an example of how to use the pyson module

# Read test
print("-----READ TEST-------")
print(pyson.getData("example.pyson", "str_example"))
print(pyson.getData("example.pyson", "int_example"))
print(pyson.getData("example.pyson", "list_example"))
print(pyson.getData("example.pyson", "float_example"))

# Whole test
print("---WHOLE TEST--------")
print(pyson.getWhole("example.pyson"))

# Write test
print("---WRITE TEST--------")
pyson.write("newfile.pyson", "string", "str", "value", "w")

# Append test
print("---APPEND TEST-------")
pyson.write("newfile.pyson", "integer", "int", 123, "a")
pyson.write("newfile.pyson", "floating-point", "float", 3.14, "a")
pyson.write("newfile.pyson", "string list", "list", ["this is a list", "of strings"])
pyson.writeMultiple("example.pyson", {"test": "value", "integer": 69, "list1": ["1", "2"], "pypi": 3.1415962})
print(pyson.getWhole("newfile.pyson"))

# Compatability test
print("---COMPATABILITY TEST------")
print(pyson.checkCompatible("example.pyson"))
print(pyson.checkCompatible("newfile.pyson"))
os.remove("newfile.pyson")

# update val test
print("---UPDATING TEST---")
pyson.updateData("example.pyson", "str_example", "this is an updated string")
print(pyson.getData("example.pyson", "str_example"))
pyson.updateData("example.pyson", "str_example", "this is a string: strings can include colons")
print(pyson.getData("example.pyson", "str_example"))
