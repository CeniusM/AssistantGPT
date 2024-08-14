# A new possible way of implementing the ChatGPT prompting

import openai
import json
from enum import Enum

from FileUtil import *

class Role:
    SYS = "system"
    USER = "user"
    AGENT = "assistant"

class AgentAction:
    TOOL = "required"
    AUTO = "auto"
    TEXT = "none"

class Prompt:
    def __init__(self,
            sys_msg: str = "",
            messages: list = [],
            agent_action: AgentAction = AgentAction.AUTO,
            tools: list = None,
            temperature: float = 0.5
        ) -> None:
        
        self.sys_msg = sys_msg
        self.messages = messages
        self.agent_action = agent_action
        self.tools = tools
        self.temperature = temperature
    
    def message(self, role: Role, content: str):
        self.messages.append({"role": role, "content": content})

class PromptResponse:
    def __init__(self) -> None:
        self.response = ""
        self.tools_called = []

class ChatGPT:
    def prompt_agent(key, prompt: Prompt) -> PromptResponse:
        # Setup
        openai.api_key = key
        result = PromptResponse()

        # Setup system message
        messages = prompt.messages.copy()
        if prompt.sys_msg:
            messages.insert(-1, {"role": Role.SYS, "content": prompt.sys_msg})
        
        # API call
        completion = openai.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = messages,
            temperature = prompt.temperature,

            # Unpack if tools are used
            **{
                "tools": [tool.__dict__() for tool in prompt.tools],
                "tool_choice": prompt.agent_action
            } if prompt.agent_action is not AgentAction.TEXT else {}
        )

        # Get api response
        message = completion.choices[0].message
        response = message.content
        tool_calls = message.tool_calls
        
        result.response = response

        # Return if no tools called
        if AgentAction.TEXT:
            return result
        
        # Parse tool calls
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool = [t for t in prompt.tools if t.name == tool_name]

            if len(tool) != 1:
                raise Exception("Tool not found")
            
            tool[0].call(tool_args)

            result.tools_called.append(tool_name)
        
        return result
        




if __name__ == "__main__":
    prompt = Prompt(
        sys_msg="Only write code",
        agent_action=AgentAction.TEXT
    )
    
    prompt.message(Role.USER, "Can you make a small python program that counts from 1 to 10")

    result = ChatGPT.prompt_agent(File.read_text("Keys\sKey"), prompt)
    
    print(result.response)
    print(result.tools_called)









# class ToolInterface:
#     def __init__(self):
#         self.name = ""
#     def call(self, args):
#         pass
#     def __dict__(self):
#         pass