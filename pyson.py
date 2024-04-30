## START OF FILE ##
def getData(filePath,datacall):
    """
    Inputs: 
    filePath - formatted like a normal file path (forward slash)
    datacall: str - name of data that you are extracting
    Outputs the data stored in pyson format that it's inserted as.
    """
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    # found is the found value
    # foundT is the found type
    found = None
    foundT = None
    # Loop through the lines in the file
    for line in open(filePath, "r").read().split("\n"):
        # split the pyson value stored into [name, type, value]
        splitted = line.split(":")
        # if correct name, fetch type & value
        if splitted[0] == datacall:
            found = splitted[2]
            foundT = splitted[1]
    # if nothing is found, raise an exception
    if found is None:
        raise Exception(f"Data At Value {datacall} Not Found. Maybe try a different file?")
    
    # Match types
    match foundT:
        case "str":
            return str(found)
        case "int":
            return int(found)
        case "float":
            return float(found)
        case "list":
            return found.split("(*)")
        case _:
            raise Exception("Unreachable, should not happen")

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
