import json

class ToolDescription:
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description
        self.params_description = ""
        self.parameters = {}
        self.required = []

    def add_parameter_description(self, description):
        self.params_description = description

    def add_parameter(self, name, arg_type, description="", required=False):
        typestr = ""

        if type(name) != str:
            raise TypeError("name is of incorrect type")
        if type(description) != str:
            raise TypeError("description is of incorrect type")
        if type(required) != bool:
            raise TypeError("required is of incorrect type")

        if arg_type == bool:
            typestr = "boolean"
        elif arg_type == int:
            typestr = "integer"
        elif arg_type == str:
            typestr = "string"
        else:
            raise TypeError("Unsupported type")
        
        param = { "type": typestr }

        if description != "":
            param["description"] = description

        self.parameters[name] = param

        if required:
            self.required.append(name)

    def to_json(self):
        func = {"name": self.name, "description": self.description}

        if len(self.parameters) != 0:
            params = {"type": "object" }

            if self.params_description != "":
                params["description"] = self.params_description

            params["properties"] = self.parameters

            if len(self.required) != 0:
                params["required"] = self.required

            func["parameters"] = params

        root = {"type": "function", "function": func}

        return json.dumps(root)

    # self[name, <required>] = type, description
    def __setitem__(self, indexer: tuple, value: tuple):

        # Value only have type, we add empty description
        if type(indexer) != tuple:
            indexer = (indexer, False)

        # Only has name, set required to false
        if type(value) != tuple:
            value = (value, "")

        elif len(indexer) != 2:
            raise Exception("Indexer must have 1 or 2 argumens")
        elif len(value) != 2:
            raise Exception("Value must have 1 or 2 argumens")

        name, is_required = indexer

        arg_type, description = value
        
        self.add_parameter(name, arg_type, description, is_required)
        
