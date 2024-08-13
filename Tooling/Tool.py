from Tooling.ToolArg import *
import json

# Defines a Tool
# - Name
# - Description
# - Args description
# - Args
# - Tool function to call
#
# It parses the arguments given by ChatGPT
# If an argument has a default value, it will replace if it is not given
#
# It also takes care of formating correctly for ChatGPT
class Tool:
    def __init__(
            self, 
            name: str, 
            function_call,
            description: str = "",
            args_description: str = "",
            args: list[ToolArg] = [],
            default_response: str = None
        ):
        self.name = name
        self.description = description
        self.args_description = args_description
        self.args = args
        self.function_call = function_call
        self.default_response = default_response

    def call(self, given_args: dict):
        # parse args
        for arg in self.args:

            # If no argument was given corresponding to the defined argument.
            # Replace it with the default
            if not arg.name in given_args or given_args[arg.name] == None:

                # If the argument was required, we raise an exception
                if arg.is_required:
                    raise Exception("No value given for required argument")

                given_args[arg.name] = arg.value
        
        if not self.args:
            # Remove args if the tool have not defined any
            response = self.function_call()
        else:
            # Call tool function with parsed arguments
            response = self.function_call(given_args)
        
        # If the tool has a default reponse we return that
        if self.default_response:
            response = self.default_response
        
        return response
    
    def __dict__(self):
        # Returns the tool as a formatted ChatGPT tool
        func = {"name": self.name }

        if self.description:
            func["description"] = self.description

        if len(self.args) != 0:
            params = {"type": "object" }

            if self.args_description != "":
                params["description"] = self.args_description


            if self.args and len(self.args) != 0:
                params["properties"] = { }

                for a in self.args:
                    params["properties"][a.name] = a.__dict__() 

            required = [arg.name for arg in self.args if arg.is_required]

            if len(required) != 0:
                params["required"] = required

            func["parameters"] = params

        root = {"type": "function", "function": func}

        return json.dumps(root)