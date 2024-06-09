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
        """String representation of the Type"""
        return self._type

    def __repr__(self) -> str:
        """
        String representation of the Type
        Unlike Type.__str__(), this method will include the fact that \
        this is a Type object from the pyson_data package
        """
        return f"pyson_data.Type({self._type})"

    def __reduce__(self) -> tuple:
        """Reduce the Type object so it can be pickled"""
        return self.__class__, (self._type,)

    def to_python_type(self) -> type:
        """
        Returns the python type of the Type
        Currently returns one of the types int, float, str, or list[str], \
        but this may change in the future if more types are added to pyson.
        """
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
        """String representation of the Value"""
        return self.pyson_str()

    def __repr__(self) -> str:
        """
        String representation of the Value
        Unlike Value.__str__(), this method will include the fact that \
        this is a Value object from the pyson_data package
        """
        return f"pyson_data.Value(type = {self._type}, value = {self._value})"

    def __reduce__(self) -> tuple:
        """Reduce the Value object so it can be pickled"""
        return self.__class__, (self._value, self._type)

    def type(self) -> Type:
        """
        Returns the pyson Type of the Value.
        Unless somebody violates python privacy conventions
        by editing the Value object directly, \
        isinstance(v.value(), v.type().to_python_type()) \
        will always be true if v is of type Value.
        """
        return self._type

    def type_str(self) -> str:
        """Returns the pyson Type of the Value as a string."""
        return self._type.__str__()

    def value(self) -> int | float | str | list[str]:
        """
        Returns the internal value contained in the Value.
        Unless somebody violates python privacy conventions
        by editing the Value object directly, \
        isinstance(v.value(), v.type().to_python_type()) \
        will always be true if v is of type Value.
        """
        return self._value

    def pyson_str(self) -> str:
        value = (
            str(self._value) if not isinstance(self._value, list)
            else "(*)".join(self._value)
        )
        return f"{self._type}:{value}"

    def is_int(self) -> bool:
        """
        Returns True if the Value is an int, False otherwise.
        If v.is_int(), then v.type_str() will return "int".
        """
        return self._type == Type("int")

    def is_float(self) -> bool:
        """
        Returns True if the Value is a float, False otherwise.
        If v.is_float(), then v.type_str() will return "float".
        """
        return self._type == Type("float")

    def is_str(self) -> bool:
        """
        Returns True if the Value is a str, False otherwise.
        If v.is_str(), then v.type_str() will return "str".
        """
        return self._type == Type("str")

    def is_list(self) -> bool:
        """
        Returns True if the Value is a list, False otherwise.
        If v.is_list(), then v.type_str() will return "list".
        """
        return self._type == Type("list")


class NamedValue:
    def __init__(self, name: str, value: Value):
        """
        Initialize a new NamedValue.
        Takes 2 arguments, which must be a str and a Value.
        """
        self._name = name
        self._value = value

    def name(self) -> str:
        return self._name

    def change_name(self, new_name: str) -> None:
        self._name = new_name

    def swap_name(self, new_name: str) -> str:
        self._name, old_name = new_name, self._name
        return old_name

    def type(self) -> Type:
        """
        Returns the type of the value in the NamedValue.
        If you have a NamedValue nv, then \
        `t = nv.type()` \
        has the same effect as \
        `t = nv.value().type()`.
        """
        return self._value.type()

    def type_str(self) -> str:
        """
        Returns the type of the value in the NamedValue as a string.
        If you have a NamedValue nv, then \
        `t = nv.type_str()` \
        has the same effect as \
        `t = nv.value().type_str()`.
        """
        return self._value.type_str()

    def value(self) -> Value:
        return self._value

    def change_value(self, new_value: Value) -> None:
        self._value = new_value

    def swap_value(self, new_value: Value) -> Value:
        self._value, old_value = new_value, self._value
        return old_value

    def to_tuple(self) -> tuple[str, Value]:
        """
        Returns a tuple of the name and value of the NamedValue.
        If you have a NamedValue nv, then \
        `name, value = nv.to_tuple()` \
        will have the same effect as \
        `name, value = nv.name(), nv.value()`.
        Additionally, if you have a str s and a value v, \
        then `s, v == NamedValue(s, v).to_tuple()` \
        will always be true.
        """
        return self._name, self._value

    def pyson_str(self) -> str:
        return f"{self._name}:{self._value}"

    def __str__(self) -> str:
        """String representation of the NamedValue"""
        return self.pyson_str()

    def __repr__(self) -> str:
        """
        String representation of the NamedValue.
        Unlike NamedValue.__str__(), this method will include the fact that \
        this is a NamedValue object from the pyson_data package
        """
        return f"pyson_data.NamedValue(name = {self._name}, value = {self._value.__repr__()})"

    def __reduce__(self) -> tuple:
        """Reduce the NamedValue object so it can be pickled"""
        return self.__class__, (self._name, self._value)


def parse_pyson_entry(entry: str) -> NamedValue:
    """
    Parse an entry (line) in pyson into a NamedValue.
    Will raise an error if the entry contains a newline, \
    or if the entry is invalid pyson.
    """
    if "\n" in entry:
        raise ValueError("pyson entries cannot contain newlines")
    name, type, value = entry.split(":", 2)
    match type:
        case "int":
            value = int(value)
        case "float":
            value = float(value)
        case "str":
            pass  # value is already a str
        case "list":
            value = value.split("(*)")
        case _:
            raise ValueError(
                f"Invalid pyson type {type} found in pyson_data.parse_pyson_entry()"
            )
    return NamedValue(name, Value(value))


def pyson_to_list(data: str) -> list[NamedValue]:
    """
    Parse a pyson string into a list of NamedValue.
    Will raise an exception if there is any invalid pyson.
    """
    list = [parse_pyson_entry(line) for line in data.split("\n") if line != ""]
    if len(set(nv.name() for nv in list)) != len(list):
        raise ValueError("Duplicate name(s) found in pyson_to_list()")
    return list


def pyson_file_to_list(file_path: str) -> list[NamedValue]:
    """
    Parse a file in the pyson format into a list of NamedValue.
    Will raise an exception if any of the following happen:
        - An IO error happens while opening or reading the file
        - The file contains invalid pyson
    """
    if not file_path.endswith(".pyson"):
        raise print("WARNING: File does not end in .pyson")
    try:
        return pyson_to_list(open(file_path, "r").read())
    except ValueError:
        raise ValueError(
            f"Duplicate name(s) found in file {file_path} during pyson_file_to_list()"
        )


def pyson_to_dict(data: str) -> dict[str, Value]:
    """
    Parse a pyson string into a dict of name (str) to value (Value).
    Will raise an exception if there is any invalid pyson.
    """
    list = [parse_pyson_entry(line) for line in data.split("\n") if line != ""]
    as_dict = dict((nv.name(), nv.value()) for nv in list)
    if len(as_dict) != len(list):
        raise ValueError("Duplicate name(s) found in pyson_to_dict()")
    return as_dict


def pyson_file_to_dict(file_path: str) -> dict[str, Value]:
    """
    Parse a pyson file into a dict of name (str) to value (Value).
    Will raise an exception if any of the following happen:
        - An IO error happens while opening or reading the file
        - The file contains invalid pyson
    """

    if not file_path.endswith(".pyson"):
        print("WARNING: File does not end in .pyson")

    try:
        return pyson_to_dict(open(file_path).read())
    except ValueError:
        raise ValueError(
            f"Duplicate name(s) found in file {file_path} during pyson_file_to_dict()"
        )


def is_valid_pyson_entry(entry: str) -> bool:
    """
    Check if a pyson entry is valid
    True = valid
    False = invalid
    Note: empty strings will be counted as invalid because \
    they are not a valid *entry* despite the fact that \
    having an empty lines is OK in the pyson format.
    """
    # this isn't great code quality or very fast
    # but if you want speed why are you using python
    # also True is definitely the happy path here
    # it is probably fine for the sad path to be slow
    try:
        parse_pyson_entry(entry)
    except ValueError:
        return False
    else:
        return True


def is_valid_pyson(data: str) -> bool:
    """
    Check if a string one or more pyson entries is valid
    True = valid
    False = invalid
    Note: having an empty line will make this function return True \
    because even though that is an invalid entry, it is still valid \
    as part of a pyson file.
    """
    return all(line == "" or is_valid_pyson_entry(line) for line in data.split("\n"))
