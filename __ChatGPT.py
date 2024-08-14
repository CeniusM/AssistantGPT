# A new possible way of implementing the ChatGPT prompting

import openai
from enum import Enum

class Role(Enum):
    sys = "system"
    user = "user"
    agent = "assistant"

class AgentAction(Enum):
    tool = "required"
    auto = "auto"
    text = "none"

class Prompt:
    def __init__(self) -> None:
        self.sys_msg: str = ""
        self.messages: list = []
        self.silent: bool = False
        self.temperature: float = 0.5
        self.ignore_response: bool = False
        self.tools: list = None
        self.agent_action: AgentAction = AgentAction.auto
    
    def message(self, role: Role, content: str):
        self.messages.append({"role": role, "content": content})

class PromptResponse:
    def __init__(self) -> None:
        self.response = ""
        self.tools_called = []
        self.action = None

class ChatGPT:
    def prompt_agent(key, prompt: Prompt) -> PromptResponse:
        openai.api_key = key

        messages = prompt.messages.copy()

        if prompt.sys_msg:
            messages.insert(-1, prompt.sys_msg)
        
        completion = openai.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = messages,
            temperature = prompt.temperature,

            # Unpack if tools are used
            **{
                "tools": [tool.__dict__() for tool in prompt.tools],
                "tool_choice": prompt.agent_action
            } if prompt.agent_action is not AgentAction.text else {}
        )

        response = completion.choices[0].message
        text = response.response
        tool_calls = response.tool_calls

        














# class ToolInterface:
#     def __init__(self):
#         self.name = ""
#     def call(self, args):
#         pass
#     def __dict__(self):
#         pass