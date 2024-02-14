import pyson # to use this in your project, simply change the name from "pyson" to the name of the file you're importing it from

# Read test
print("-----READ TEST-------")
print(pyson.pn2GetData("config.cnf","str_example"))
print(pyson.pn2GetData("config.cnf","int_example"))
print(pyson.pn2GetData("config.cnf","list_example"))

# Whole test
print("---WHOLE TEST--------")
print(pyson.pn2GetWhole("config.cnf"))

# Append test
print("---APPEND TEST-------")
pyson.pn2Write("config.cnf","write_example","list",["this","is","a","new","list"])
print(pyson.pn2GetData("config.cnf","write_example"))

# Compatability test
print("---COMPATABILITY TEST------")
print(pyson.checkCompatible("config.cnf"))
