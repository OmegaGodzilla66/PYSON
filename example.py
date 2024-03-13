import pyson # to use this in your project, simply change the name from "pyson" to the name of the file you're importing it from

# Read test
print("-----READ TEST-------")
print(pyson.getData("example.pyson","str_example"))
print(pyson.getData("example.pyson","int_example"))
print(pyson.getData("example.pyson","list_example"))

# Whole test
print("---WHOLE TEST--------")
print(pyson.getWhole("example.pyson"))

# Append test
print("---APPEND TEST-------")
pyson.write("example.pyson","write_example","list",["this","is","a","new","list"])
print(pyson.getData("example.pyson","write_example"))

# Compatability test
print("---COMPATABILITY TEST------")
print(pyson.checkCompatible("example.pyson"))
