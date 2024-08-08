import json

class ToolDescription:
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description
        self.params_description = ""
        self.parameters = []
        self.required = []

    def add_parameter_description(self, description):
        self.params_description = description

    def add_required_parameter(self, name, type, description=""):
        self.add_parameter(name, type, description)
        self.required.append(name)

    def add_parameter(self, name, type, description=""):
        typestr = ""

        if type == bool:
            typestr = "boolean"
        elif type == int:
            typestr = "integer"
        elif type == str:
            typestr = "string"
        else:
            raise TypeError("Unsupported type")

        self.parameters.append(name, typestr, description)

    def to_json(self):
        func = {"name": self.name, "description": self.description}

        if len(self.parameters) != 0:
            params = {"type": "object", "description": self.params_description, "properties": self.parameters}

            func["parameters"] = params

        root = {"type": "function", "function": func}

        return json.dumps(root)

