from NewTooling.ToolArg import *
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
            description: str,
            args_description: str,
            args: list[ToolArg],
            function_call: function,
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
        for key, value in self.args:

            # If no argument was given corresponding to the defined argument.
            # Replace it with the default
            if not key in given_args:

                # If the argument was required, we raise an exception
                if value.is_required:
                    raise Exception("No value given for required argument")

                given_args[key] = value.value

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

            params["properties"] = self.args

            required = [arg.name for arg in self.args if arg.is_required]

            if len(required) != 0:
                params["required"] = required

            func["parameters"] = params

        root = {"type": "function", "function": func}

        return json.dumps(root)