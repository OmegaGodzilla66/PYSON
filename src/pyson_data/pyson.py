class Type:
    def __init__(self, type) -> None:
        """
        Initialize a new pyson Type
        Takes 1 argument, which must be either "int", "float", "str", or "list"
        """
        if type not in ["int", "float", "str", "list"]:
            raise ValueError(f"Invalid type {type}")
        self.type: str = type

    def __str__(self) -> str:
        """
        String representation of the Type
        """
        return self.type

    def __repr__(self) -> str:
        """
        String representation of the Type
        Unlike Type.__str__(), this method will include the fact that
        this is a Type object from the pyson_data package
        """
        return f"pyson_data.Type({self.type})"

    def __reduce__(self) -> tuple:
        """
        Reduce the Type object so it can be pickled
        """
        return (self.__class__, (self.type,))

class Value:
    def __init__(self, value: int | float | str | list[str]) -> None:
        """
        Initialize a new pyson Value
        Takes 1 argument, which must be either an int, float, str, or list of str
        """
        self.value: int | float | str | list[str] = value
        if isinstance(value, int):
            self.type = Type("int")
        elif isinstance(value, float):
            self.type = Type("float")
        elif isinstance(value, str):
            self.type = Type("str")
        elif isinstance(value, list):
            if any(not isinstance(item, str) for item in value):
                raise ValueError("Lists in pyson must contain only strings")
            self.type = Type("list")
        else:
            raise ValueError(f"Invalid pyson type type {type(value)}")

    def __str__(self) -> str:
        """
        String representation of the Value
        """
        return f"{self.type}:{self.value}"

    def __repr__(self) -> str:
        """
        String representation of the Value
        Unlike Value.__str__(), this method will include the fact that
        this is a Value object from the pyson_data package
        """
        return f"pyson_data.Value(type = {self.type}, value = {self.value})"

    def __reduce__(self) -> tuple:
        """
        Reduce the Value object so it can be pickled
        """
        return (self.__class__, (self.value, self.type))