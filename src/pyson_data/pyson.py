# Values in pyson can be strings, lists of strings, floating-point numbers, or integers
PysonValue = str | list[str] | float | int


def getData(filepath: str, name: str) -> PysonValue:
    """
    Parameters:
        filepath: str - formatted like a normal file path (forward slash)
        name: str - name of data that you are extracting
    Return value: the value from the pyson file with name from the name parameter
    """

    # Raise an exception if the file is not pyson-compatible
    if not checkCompatible(filepath):
        raise Exception("File is not compatible with .pyson format.")

    # Loop through the lines in the file
    for line in open(filepath, "r").read().split("\n"):
        if line == "":
            continue
        # Split the pyson value stored into [name, type, value]
        data = line.split(":", 2)
        # If the name is correct, store the value and type
        if data[0] == name:
            match data[1]:
                case "str":
                    return str(data[2])
                case "int":
                    return int(data[2])
                case "float":
                    return float(data[2])
                case "list":
                    return data[2].split("\n")
                case _:
                    raise Exception("Should be unreachable due to checkCompatible")
    # If the name desired is not in the file, raise an exception
    raise Exception(f"Data with name \"{name}\" not found. Maybe try a different file?")


def getWhole(filepath: str) -> list[PysonValue]:
    """
    Parameters:
        filepath: str - the file to get all the pyson values from
    Return value:
        A list of all the pyson values from the file
    """

    # Checks whether the file is valid pyson
    if not checkCompatible(filepath):
        raise Exception("File passed to getWhole() is not compatible with pyson format")

    whole: list[PysonValue] = []
    for item in open(filepath, "r").read().split("\n"):
        if item == "":
            continue
        data: list[str] = item.split(":", 2)
        match data[1]:
            case "str":
                whole.append(data[2])
            case "int":
                whole.append(int(data[2]))
            case "float":
                whole.append(float(data[2]))
            case "list":
                whole.append(data[2].split("(*)"))
            case _:
                raise Exception(f"Unknown type {data[1]} in {filepath} found during getWhole()")
    return whole


# Append pyson value to pyson file
# TODO: optimize
def write(filepath: str, name: str, type: str, value: PysonValue, mode: str = "a") -> None:
    """
    Parameters:
        filepath: str - File path to write to
        name: str - Name of the PysonValue to write
        type: str - Type of the PysonValue to write
        value: PysonValue - Value to insert into the file
        mode (optional):  str- What mode to use when writing the file.
    `mode` can be either 'w' (overwrite old data) or 'a' (append to the file), defaults to 'a'.
    Return value: None
    """

    # Create the file if it doesn't exist
    open(filepath, "a+").close()

    # Make value be a str
    if isinstance(value, list):
        value = "(*)".join(value)
    if isinstance(value, float) or isinstance(value, int):
        value = str(value)
    if not isinstance(value, str):
        raise Exception("Parameter value has invalid type")

    # Make sure the write mode is either append or write
    if not (mode == "a" or mode == "w"):
        raise Exception("Invalid writing mode, must be 'a' (append) or 'w' (write)")
    # Checks for .pyson compatability
    if not checkCompatible(filepath):
        raise Exception("File is not compatible with .pyson format.")

    fileData: list[str] = open(filepath, "r").read().split("\n")
    names: list[str] = []

    data = ""
    for item in fileData:
        if item == "":
            continue
        data = item.split(":", 2)
        match data[1]:
            case "str" | "int" | "list" | "float":
                names.append(data[0])
            case _:
                raise Exception("Unreachable, type correctness is checked in checkCompatible()")
    if name in names:
        raise Exception("Cannot have two items with the same call.")
    # Checks for .pyson compatability with the new item
    match type:
        case "str" | "list":
            pass
        case "int":
            # Make sure the value is actually an int
            int(value)
        case "float":
            # Make sure the value is actually a float
            float(value)
        case _:
            raise Exception(f"Data type {type} not supported")
    toWrite = name + ":" + type + ":" + value
    if mode == "a":
        toWrite = "\n" + toWrite
    open(filepath, mode).write(toWrite)


def writeMultiple(filepath: str, data: dict[str, PysonValue], mode: str = "a") -> None:
    """
    Parameters:
        filepath: str - File path to write to
        data: dict[str, PysonValue] - Dictionary of {name : value}
        mode (optional):  str- What mode to use when writing the file.
    `mode` can be either 'w' (overwrite old data) or 'a' (append to the file), defaults to 'a'.
    Return value: None
    """
    for tup in data.items():
        name, value = tup
        type = ""
        if isinstance(value, list):
            type = "list"
        if isinstance(value, int):
            type = "int"
        if isinstance(value, float):
            type = "float"
        if isinstance(value, str):
            type = "str"
        if type == "":
            raise Exception("Invalid pyson typein writeMultiple()")
        write(filepath, name, type, value, mode)
        mode = "a"


def updateData(filepath: str, name: str, data: str) -> None:
    """
    Note: the type of data currently cannot be updated
    Parameters:
        filepath: str - File path where the value is
        name: str - Name of the data to update
        data: str - The value to update as a string
    Return value: None
    """
    data = str(data)
    # Read in the data
    file = open(filepath, "r")
    fileData: list[str] = file.read().split("\n")
    file.close()
    # Look through the data to find the value to update
    index: int = 0
    foundItem: bool = False
    for line in fileData:
        splitted: list[str] = line.split(":", 2)
        if splitted[0] == name:
            splitted[2] = data
            fileData[index] = ":".join(splitted)
            foundItem = True
            break
        index += 1
    # If no value had the desired name, raise an exception
    if not foundItem:
        raise Exception("Couldn't write to non-existent item")
    # Write out the data
    open(filepath, "w").write("\n".join(fileData))


# Returns `true` if the file at filePath is a valid pyson file, and false otherwise.
def checkCompatible(filepath: str) -> bool:
    """
    Parameters:
        filepath: str - Path to the file that you want to check whether it is compatible
    Return value:
        True if the file at filePath is valid pyson
        False if the file at filePath is not valid pyson
    """

    fileData: list[str] = open(filepath, "r").read().split("\n")
    names: set[str] = set()
    # Go through the items, check if they have correct types, and if it is [dataname, type, value]
    for item in fileData:
        if item == "":
            continue
        data = item.split(":", 2)
        if len(data) < 3:
            return False
        match data[1]:
            case "str" | "list":
                pass
            case "int":
                try:
                    int(data[2])
                except ValueError:
                    return False
            case "float":
                try:
                    float(data[2])
                except ValueError:
                    return False
            case _:
                return False
        if data[0] in names:
            return False
        names.add(data[0])

    return True
