# Values in pyson can be strings, lists of strings, floating-point numbers, or integers
PysonValue = str | list[str] | float | int


def getData(filePath: str, name: str) -> PysonValue:
    """Extracts a single item's value from a .pyson file
    
    Args:
        filepath (str): Filepath location of pyson file 
        name (str): Name of data that you are extracting
        
    Returns: 
        PysonValue: The value of the item you extracted from the pyson file
    """

    # Raise an exception if the file is not pyson-compatible
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    # Loop through the lines in the file
    for line in open(filePath, "r").read().split("\n"):
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


def getList(filePath: str) -> list[PysonValue]:
    """Extracts all values of items from a .pyson file in list format
    
    Args:
        filePath (str): the file to extract the pyson values from
        
    Returns:
        list: A list of all the pyson values from the file
    """

    # Checks whether the file is valid pyson
    if not checkCompatible(filePath):
        raise Exception("File passed to getList() is not compatible with pyson format")

    whole: list[PysonValue] = []
    for item in open(filePath, "r").read().split("\n"):
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
                raise Exception(f"Unknown type {data[1]} in {filePath} found during getList()")
    return whole

def getDict(filePath: str) -> dict[str, PysonValue]:
    """Fetches all items from a .pyson file and returns a hashmap of {name:value}
    
    Args:
        filePath (str): the file to extract values from
    
    Returns:
        dict: A dict of {name : value} with all the pyson values from the file 
    """

    if not checkCompatible(filePath):
        raise Exception("File passed to getDict() is not compatible with the pyson format")

    data: dict[str, PysonValue] = dict()
    for line in open(filePath, "r").read().split("\n"):
        if line == "":
            continue
        name, type, value = line.split(":", 2)
        match type:
            case "str":
                data[name] = value
            case "int":
                data[name] = int(value)
            case "float":
                data[name] = float(value)
            case "list":
                data[name] = value.split("(*)")
            case _:
                raise Exception(f"Unknown type {type} in {filePath} found during getDict()")
    return data
    

# Append pyson value to pyson file
# TODO: optimize
def write(filePath: str, name: str, type: str, value: PysonValue, mode: str = "a") -> None:
    """Writes/appends single value to .pyson file
    
    Args:
        filepath (str): File path to write to
        name (str): Name of the PysonValue to write
        type (str): Type of the PysonValue to write
        value (PysonValue): Value to insert into the file
        mode (str):  What mode to use when writing the file.
            mode can be either 'w' (overwrite old data) or 'a' (append to the file)
            (default is 'a')
            
    Returns: 
        None
    """

    # Create the file if it doesn't exist
    open(filePath, "a+").close()

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
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    fileData: list[str] = open(filePath, "r").read().split("\n")
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
    open(filePath, mode).write(toWrite)


def writeMultiple(filePath: str, data: dict[str, PysonValue], mode: str = "a") -> None:
    """Writes/appends multiple pyson values to a file
    
    Args:
        filepath (str): File path to write to
        data (dict[str, PysonValue]): Dictionary of {name : value}
         mode (str):  What mode to use when writing the file.
            mode can be either 'w' (overwrite old data) or 'a' (append to the file)
            (default is 'a')
    
    Returns: 
        None
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
            raise Exception("Invalid pyson type in writeMultiple()")
        write(filePath, name, type, value, mode)
        mode = "a"


def updateData(filePath: str, name: str, data: str) -> None:
    """Updates value of item in .pyson file
    Note: the type of data currently cannot be updated
    
    Args:
        filepath (str): File path where the value is
        name (str): Name of the data to update
        data (str): The value to update as a string
        
    Returns: None
    """
    data = str(data)
    # Read in the data
    file = open(filePath, "r")
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
    open(filePath, "w").write("\n".join(fileData))


# Returns `true` if the file at filePath is a valid pyson file, and false otherwise.
def checkCompatible(filePath: str) -> bool:
    """Checks if file is compatible with .pyson format
    
    Args:
        filepath (str): Path to the file that you want to check whether it is compatible
    Returns:
        bool: a bool that indicates whether or not a file is valid pyson
    """

    fileData: list[str] = open(filePath, "r").read().split("\n")
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
