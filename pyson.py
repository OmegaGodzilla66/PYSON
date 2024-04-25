## START OF FILE ##
def getData(filePath,datacall):
    """Inputs: 
    filePath - folder/file.pyson (note: can have multiple folder paths, however file MUST use pyson-type file configuration.
    datacall: str - name of data that you are extracting
    Outputs the data stored in pyson format that it's inserted as."""
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")
    # start lost and found
    lost = open(filePath, "r").read().split("\n")
    found = None
    foundT = None
    for i in range(len(lost)):
        if lost[i].split(":")[0] == datacall:
            found = lost[i].split(":")[2]
            foundT = lost[i].split(":")[1]

    if found is None:
        raise Exception(f"Data At Value {datacall} Not Found. Maybe try a different file?")
    # End lost and found

    if foundT is None:
        raise Exception("This should never happen file was already verified to be correct")

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
            raise Exception(f"""Data type {foundT} not supported""")


def getWhole(filePath):
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with pyson format.")
    wholeRAW = open(filePath,"r").read().split("\n")
    whole = []
    for item in wholeRAW:
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
                print("ERROR FOUND AT UNKNOWN DATA")
                raise Exception(f"""Unknown data {data[1]} type found in {filePath} at call {data[0]}. Raw pyson data: {item}. Try checking if you have any external plugins that may be interfearing with the pyson format. Or, if you entered the data manually, check if you made a typo. """)

    return whole

def write(filePath: str, datacall, datatype, data):
    # Checks for .pyson compatability
    to_append = data
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")

    # Checks for duplicates
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
            val = to_append.join("(*)")
        case _:
            raise Exception(f"Data type {datatype} not supported")
    toWrite = "\n" + datacall + ":" + datatype + ":" + val
    with open(filePath, "a") as a:
        a.write(toWrite)

def checkCompatible(filePath: str):
    file = open(filePath,"r").read().split("\n")
    whole = []
    
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

    if duplications(whole):
        print("ERROR: Duplications present in pyson file.")
        return False
    
    return True        


def duplications(seq):
    hash_table = {}
    for item in list:
        if item in hash_table:
            return True
        hash_table[item] = True
    return False
## END OF FILE ##
