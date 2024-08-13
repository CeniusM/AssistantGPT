
class ToolArg:
    def __init__(self, name, py_type=str, description=None):
        self.name = name
        self.type = py_type
        self.description = description
        self.is_required = False
        self.value = None

    def describe(self, description):
        self.description = description
        return self

    def required(self):
        if self.value:
            raise Exception("Argument can not be required if it has a default value")

        self.is_required = True
        return self
    
    def default(self, value):
        if self.is_required:
            raise Exception("Argument can not have a default value when it is required")

        self.value = value
        return self
    
    def __dict__(self):
        # Formats the tool argument as formatted for ChatGPT
        type_str = { 
            bool: "boolean", 
            str: "string", 
            int: "integer"
        }[self.type]

        formatted =  { "type": type_str } 

        if self.description:
            formatted["description"] = self.description

        return formatted