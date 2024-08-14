# A new possible way of implementing the ChatGPT prompting

import openai
import json

from FileUtil import *

class ToolInterface:
    def __init__(self):
        self.name = ""
    def call(self, args):
        pass
    def __dict__(self):
        pass

class Role:
    SYS = "system"
    USER = "user"
    AGENT = "assistant"

class AgentAction:
    TOOL = "required"
    AUTO = "auto"
    TEXT = "none"

class Agent_GPT:
    def __init__(self,
            key,
            sys_msg: str = None,
            messages: list = [],
            agent_action: AgentAction = AgentAction.AUTO,
            tools: list[ToolInterface] = None,
            temperature: float = 0.5
        ) -> None:
        
        self.key = key
        self.sys_msg = sys_msg
        self.messages = messages
        self.agent_action = agent_action
        self.tools = tools
        self.temperature = temperature
        
    def message(self, role: Role, content: str):
        self.messages.append({"role": role, "content": content})

    def prompt_agent(self):
        # Setup
        openai.api_key = self.key

        # Setup system message
        messages = self.messages
        if self.sys_msg:
            messages.insert(-1, {"role": Role.SYS, "content": self.sys_msg})
        
        # API call
        completion = openai.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = messages,
            temperature = self.temperature,

            # Unpack if tools are used
            **{
                "tools": [tool.__dict__() for tool in self.tools],
                "tool_choice": self.agent_action
            } if self.agent_action is not AgentAction.TEXT else {}
        )

        # Get api response
        message = completion.choices[0].message
        response = message.content
        tool_calls = message.tool_calls

        # Return if no tools called
        if AgentAction.TEXT:
            return (response, None)
        
        tools_called = []
        
        # Parse tool calls
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool = [t for t in self.tools if t.name == tool_name]

            if len(tool) != 1:
                raise Exception("Tool not found")
            
            tool[0].call(tool_args)

            tools_called.append(tool_name)
        
        return (response, tools_called)
        




if __name__ == "__main__":
    agent = Agent_GPT(
        sys_msg="Only write code",
        agent_action=AgentAction.TEXT
    )
    
    agent.message(Role.USER, "Can you make a small python program that counts from 1 to 10")

    result = agent.prompt_agent()
    
    print(result.response)
    print(result.tools_called)

