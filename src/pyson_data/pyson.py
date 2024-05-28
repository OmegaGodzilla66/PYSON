class Type:
    def __init__(self, type) -> None:
        """
        Initialize a new pyson Type
        Takes 1 argument, which must be either "int", "float", "str", or "list"
        """
        if type not in ["int", "float", "str", list]:
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
        return (Type, (self.type,))