def getData(filePath, name) -> str | list[str] | float | int:
    """
    Inputs: 
    filePath - formatted like a normal file path (forward slash)
    name: str - name of data that you are extracting
    Returns the value from the pyson file with the desired name
    """
    # Raise an exception if the file is not pyson-compatible
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    foundValue = None
    foundType = None
    # Loop through the lines in the file
    for line in open(filePath, "r").read().split("\n"):
        # Split the pyson value stored into [name, type, value]
        splitted = line.split(":")
        # If the name is correct, store the value and type
        if splitted[0] == name:
            foundValue = splitted[2]
            foundType = splitted[1]
            break
    # If the name desired is not in the file, raise an exception
    if foundValue is None:
        raise Exception(f"Data with name \"{name}\" not found. Maybe try a different file?")
    
    # Check what type it is
    match foundType:
        case "str":
            return str(foundValue)
        case "int":
            return int(foundValue)
        case "float":
            return float(foundValue)
        case "list":
            return foundValue.split("(*)")
        case _:
            raise Exception(f"Invalid pyson type {foundType}")

# get all of the file, returned as an array of values
def getWhole(filePath):
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with pyson format.")
    whole = []
    for item in open(filePath,"r").read().split("\n"):
        data = item.split(":")
        match data[1]:
            case "str":
                whole.append(str(data[2]))
            case "int":
                whole.append(int(data[2]))
            case "float":
                whole.append(float(data[2]))
            case "list":
                whole.append(data[2].split("(*)"))
            case _:
                print("ERROR: Unknown Datatype")
                raise Exception(f"""Unknown data {data[1]} type found in {filePath} at call {data[0]}. Raw pyson data: {item}. Try checking if you have any external plugins that may be interfering with the pyson format. Or, if you entered the data manually, check if you made a typo. """)

    return whole


# append pyson value to pyson file
# TODO: optimize
def write(filePath: str, datacall, datatype, data, mode = "a"):
    if not (mode == "a" or mode == "w"):
        raise Exception("invalid mode, must be 'a' or 'w'")
    # Checks for .pyson compatability
    to_append = data
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    file = open(filePath,"r").read().split("\n")
    calls = []

    for item in file:
        data = item.split(":")
        match data[1]:
            case "str" | "int" | "list" | "float":
                calls.append(data[0])
            case _:
                print("ERROR FOUND AT UNKNOWN DATA")
                return False
    if datacall in calls:
        raise Exception("Cannot have two items with the same call.")
    # Checks for .pyson compatability with the new item
    val = "" # empty placeholder so we don't mess with scope errors 
    match datatype:
        case "str":
            val = to_append
        case "int":
            val = int(to_append)
        case "float":
            val = float(to_append)
        case "list":
            val = "(*)".join(to_append)
        case _:
            raise Exception(f"Data type {datatype} not supported")
    toWrite = "\n" + datacall + ":" + datatype + ":" + val
    with open(filePath, mode) as f:
        f.write(toWrite)



def updateData(filePath, datacall, data):
    # loop through file
    file = open(filePath, "r")
    fileData = file.read().split("\n")
    file.close()
    index = 0
    foundItem = False
    for line in fileData:
        splitted = line.split(":")
        if splitted[0] == datacall:
            splitted[2] = data
            fileData[index] = ":".join(splitted)
            foundItem = True
            break
        index += 1
    if not foundItem:
        raise Exception("couldn't write to non-existent item")
    # write to file
    open(filePath, "w").write("\n".join(fileData))
    return True
    
    
            
        
# checks if file is compatible with pyson formatting

def checkCompatible(filePath: str):
    file = open(filePath,"r").read().split("\n")
    whole = []
    # go through the items, check if they have correct types, and if there it is [dataname, type, value]
    for item in file:
        data = item.split(":")
        if len(data) != 3:
            print("ERROR FOUND IN FORMATTING")
            return False
        match data[1]:
            case "str" | "int" | "list" | "float":
                whole.append(data[0])
            case _:
                print("ERROR FOUND AT UNKNOWN DATA")
                return False
    # check for duplications
    if duplications(whole):
        print("ERROR: Duplications present in pyson file.")
        return False
    
    return True
# returns true if duplications, false if none
def duplications(seq):
    hash_table = {}
    for item in seq:
        if item in hash_table:
            return True
        hash_table[item] = True
    return False
## END OF FILE ##
