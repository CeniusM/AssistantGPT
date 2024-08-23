import openai
import json
from Chat import *
from ModelsDefined import *

class ToolChoice:
    TOOL = "required"
    AUTO = "auto"
    NONE = "none"

class Prompt:
    def __init__(self, chat: Chat, available_tools = None, force_tool_call = False, temperature = 0.5):
        self.chat = chat
        self.available_tools = available_tools
        self.temperature = temperature

        if force_tool_call:
            self.tool_choice = ToolChoice.TOOL
        elif available_tools:
            self.tool_choice = ToolChoice.AUTO
        else:
            self.tool_choice = ToolChoice.NONE
    
    # Returns the prompt as paramerters the openai can use
    def get_packed_parameters(self):
        parameters = {}

        parameters["temperature"] = self.temperature
        parameters["messages"] = self.chat.format()

        if self.tool_choice is not ToolChoice.NONE and self.available_tools:
            parameters["tools"] = self.available_tools
            parameters["tool_choice"] = self.tool_choice

        return parameters

class Response:
    def __init__(self, message, response, tool_calls, cost) -> None:
        self.message = message
        self.response = response
        self.tool_calls = tool_calls
        self.cost = cost
        self.no_tools_called = not tool_calls

class ChatGPT:
    def set_api_key(key: str):
        openai.api_key = key

    def call_api(model: Model, prompt: Prompt):
        completion = openai.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                
                **prompt.get_packed_parameters()
            )
        
        input_cost = model.input_price * completion["usage"]["prompt_tokens"]
        output_cost = model.output_price * completion["usage"]["completion_tokens"]
        cost = input_cost + output_cost

        message = completion.choices[0].message
        response = message.content

        tool_calls = None

        if message.tool_calls:
            tool_calls = []
            for call in message.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments)
                tool_calls.append({
                    "name": name,
                    "args": args
                })
        
        return Response(message, response, tool_calls, cost)

if __name__ == "__main__":
    # Set global api key
    ChatGPT.set_api_key("1234")

    # Should be stored some where for easy access
    model = Model("gpt-3.5-turbo-0125", 0.5, 1.5)

    # Chat
    chat = Chat()
    
    chat.message(Role.USER, "Can you say hi")
    chat.message(Role.AGENT, "Hi!")
    chat.message(Role.USER, "Make a program to count from 1 to 10")

    # Make prompt
    prompt = Prompt()

    # Call api
    response = ChatGPT.call_api(model, prompt)