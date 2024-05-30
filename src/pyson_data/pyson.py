class Type:
    def __init__(self, type) -> None:
        """
        Initialize a new pyson Type
        Takes 1 argument, which must be either "int", "float", "str", or "list"
        """
        if type not in ["int", "float", "str", "list"]:
            raise ValueError(f"Invalid type {type}")
        self._type: str = type

    def __str__(self) -> str:
        """
        String representation of the Type
        """
        return self._type

    def __repr__(self) -> str:
        """
        String representation of the Type
        Unlike Type.__str__(), this method will include the fact that
        this is a Type object from the pyson_data package
        """
        return f"pyson_data.Type({self._type})"

    def __reduce__(self) -> tuple:
        """
        Reduce the Type object so it can be pickled
        """
        return (self.__class__, (self._type,))

    def to_python_type(self) -> type:
        match self._type:
            case "int":
                return int
            case "float":
                return float
            case "str":
                return str
            case "list":
                return list[str]
        assert False, f"Unreachable code: pyson_data.Type with invalid type {self._type}"

class Value:
    def __init__(self, value: int | float | str | list[str]) -> None:
        """
        Initialize a new pyson Value
        Takes 1 argument, which must be either an int, float, str, or list of str
        """
        self._value: int | float | str | list[str] = value
        if isinstance(value, int):
            self._type = Type("int")
        elif isinstance(value, float):
            self._type = Type("float")
        elif isinstance(value, str):
            self._type = Type("str")
        elif isinstance(value, list):
            if any(not isinstance(item, str) for item in value):
                raise ValueError("Lists in pyson must contain only strings")
            self._type = Type("list")
        else:
            raise ValueError(f"Invalid pyson type type {type(value)}")

    def __str__(self) -> str:
        """
        String representation of the Value
        """
        return f"{self._type}:{self._value}"

    def __repr__(self) -> str:
        """
        String representation of the Value
        Unlike Value.__str__(), this method will include the fact that
        this is a Value object from the pyson_data package
        """
        return f"pyson_data.Value(type = {self._type}, value = {self._value})"

    def __reduce__(self) -> tuple:
        """
        Reduce the Value object so it can be pickled
        """
        return (self.__class__, (self._value, self._type))

    def type(self) -> Type:
        return self._type

    def type_str(self) -> str:
        return self._type.__str__()

    def value(self) -> int | float | str | list[str]:
        return self._value

    def pyson_str(self) -> str:
        value = (
            str(self._value) if not isinstance(self._value, list)
            else "(*)".join(self._value)
        )
        return f"{self._type}:{value}"

    def is_int(self) -> bool:
        return self._type == Type("int")

    def is_float(self) -> bool:
        return self._type == Type("float")

    def is_str(self) -> bool:
        return self._type == Type("str")

    def is_list(self) -> bool:
        return self._type == Type("list")

NamedValue = tuple[str, Value]

def parse_pyson_entry(entry: str) -> NamedValue:
    if "\n" in entry:
        raise ValueError("pyson entries cannot contain newlines")
    name, type, value = entry.split(":", 2)
    match type:
        case "int":
            value = int(value)
        case "float":
            value = float(value)
        case "str":
            pass    # value is already a str
        case "list":
            value = value.split("(*)")
        case _:
            raise ValueError(
                f"Invalid pyson type {type} found in pyson_data.parse_pyson_entry()"
            )
    return (name, Value(value))

def pyson_to_list(data: str) -> list[NamedValue]:
    list = [parse_pyson_entry(line) for line in data.split("\n")]
    if len(set(name for name, value in list)) != len(list):
        raise ValueError("Duplicate name(s) found in pyson_to_list()")
    return list

def pyson_file_to_list(file_path: str) -> list[NamedValue]:
    try:
        return pyson_to_list(open(file_path, "r").read())
    except ValueError:
        raise ValueError(
            f"Duplicate name(s) found in file {file_path} during pyson_file_to_list()"
        )

def pyson_to_dict(data: str) -> dict[str, Value]:
    list = [parse_pyson_entry(line) for line in data.split("\n")]
    as_dict = dict(list)
    if len(as_dict) != len(list):
        raise ValueError("Duplicate name(s) found in pyson_to_dict()")
    return as_dict

def pyson_file_to_dict(file_path: str) -> dict[str, Value]:
    try:
        return pyson_to_dict(open(file_path).read())
    except ValueError:
        raise ValueError(
            f"Duplicate name(s) found in file {file_path} during pyson_file_to_dict()"
        )