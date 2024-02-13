## START OF FILE ##
def getData(filePath,datacall):
    """Inputs: 
    filePath - folder/file.pyson (note: can have multiple folder paths, however file MUST use pyson-type file configuration.
    datacall: str - name of data that you are extracting
    Outputs the data stored in pyson format that it's inserted as."""
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")
        return # just to be safe
    # start lost and found
    lost=open(filePath, "r").read().split("\n")
    found=None
    for i in range(len(lost)):
        if lost[i].split(":")[0]==datacall:
            found=lost[i].split(":")[2]
            fountT=lost[i].split(":")[1]

    if found==None:
        raise Exception(f"Data At Value {datacall} Not Found. Maybe try a different file?")
        return # just in case
    # End lost and found

    match fountT:
        case "str":
            return str(found)
        case "int":
            return int(found)
        case "list":
            return found.split("(*)")
        case _:
            raise Exception(f"""Data type {foundT} not supported""")
            return # just in case


def getWhole(filePath):
    # Checks for .pyson compatability
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with pyson format.")
        return # just to be safe
    wholeRAW=open(filePath,"r").read().split("\n")
    whole=[]
    for item in wholeRAW:
        data=item.split(":")
        match data[1]:
            case "str":
                whole.append(str(data[2]))
            case "int":
                whole.append(int(data[2]))
            case "list":
                whole.append(data[2].split("(*)"))
            case _:
                print("ERROR FOUND AT UNKNOWN DATA")
                raise Exception(f"""Unknown data {data[1]} type found in {filePath} at call {data[0]}. Raw pyson data: {item}. Try checking if you have any external plugins that may be interfearing with the pyson format. Or, if you entered the data manually, check if you made a typo. """)
                return # just in case

    return whole

def write(filePath, datacall, datatype, data):
    # Checks for .pyson compatability
    ddata=data # Wahoo! A return to PN naming congentions! Gotta love that!
    if not checkCompatible(filePath):
        raise Exception("File is not compatible with .pyson format.")
        return # just to be safe

    # Checks for duplicates
    file=open(filePath,"r").read().split("\n")
    calls=[]

    for item in file:
        data=item.split(":")
        match data[1]:
            case "str":
                calls.append(data[0])
            case "int":
                calls.append(data[0])
            case "list":
                calls.append(data[0])
            case _:
                print("ERROR FOUND AT UNKNOWN DATA")
                return False
    if duplications(calls,datacall): raise Exception("Cannot have two items with the same call.")
    # Checks for .pyson compatability with the new item
    if not checkCompatible:
        raise Exception("File is not compatible with .pyson format.")
    match datatype:
        case "str":
            toWrite="\n"+datacall+":"+datatype+":"+ddata
        case "int":
            toWrite="\n"+datacall+":"+datatype+":"+int(ddata)
        case "list":
            lst=""
            for i in range(0,len(ddata)-1):
                lst+=ddata[i]+"(*)"
            lst+=ddata[-1]
            toWrite="\n"+datacall+":"+datatype+":"+lst
        case _:
            raise Exception(f"""Data type {datatype} not supported""")
            return # just in case

    with open(filePath, "a") as a: a.write(toWrite)

def checkCompatible(filePath):
    file=open(filePath,"r").read().split("\n")
    whole=[]
    calls=[]
    
    for item in file:
        data=item.split(":")
        try:
            data[0]
            data[1]
            data[2]
        except:
            print("ERROR FOUND IN FORMATTING")
            return False
        match data[1]:
            case "str":
                whole.append(data[0])
            case "int":
                whole.append(data[0])
            case "list":
                whole.append(data[0])
            case _:
                print("ERROR FOUND AT UNKNOWN DATA")
                return False


    if duplications(whole):
        print("ERROR: Duplications present in pyson file.")
        return False
    
    return True        


def duplications(seq,app=None):
    if app!=None:
        seq.append(app)
    seen = []
    unique_list = [x for x in seq if x not in seen and not seen.append(x)]
    return len(seq) != len(unique_list)
## END OF FILE ##
