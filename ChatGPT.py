import openai

from ConsoleHelper import *
from KeyManager import *

class ChatGPT:
    total_cost = 0

    def prompt(
            conversation_history,
            temperature=0.5,
            silent=True,
            tools_json = None,
            tool_choice = None):
        
        openai.api_key = get_GPT_key()

        # OpenAI API call
        completion = openai.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = conversation_history,
                temperature = temperature,
                
                # Create a dictionary with optional tool parameters if they are given
                **{
                    "tools": tools_json,
                    "tool_choice": tool_choice
                } if tools_json else {}
            )
    
        total_tokens = completion.usage.total_tokens
        cost = round((total_tokens*0.002)/1000, 10)
        ChatGPT.total_cost = round(ChatGPT.total_cost + cost, 10)
        
        message = completion.choices[0].message
        response = message.content
        tool_calls = message.tool_calls

        if response and not silent:
            color(ConsoleColor.BOLD)
            color(ConsoleColor.OKCYAN)
            print_checked(f"\n{response}\n")

        # If no tools were given, we just return the response
        if not tools_json:
            return response
        else:
            return response, tool_calls, message

    def smart_prompt(conversation_history, tools=None, temperature=0.5, silent=False):

        # Note. This could be a parameter, then when calling the smart prompt,
        # the GPT agent could have acces to diffrent tools, and thereby specialising the agents 
        # available_tools, tools_json = get_available_tools()
        
        response, tool_calls, message = ChatGPT.prompt(
                                        conversation_history=conversation_history,
                                        temperature=temperature,
                                        silent=silent,
                                        tools_json=[a.__dict__() for a in tools],
                                        tool_choice="auto"
                                    )
        
        # check if the model wanted to call a function, if not, return
        if not tool_calls:
           return response
        
        user_input = conversation_history[0]["content"]
        conversation_history.append(message)  # extend conversation with assistant's reply    ¯\_(ツ)_/¯

        # Send the info for each function call and function response to the model
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool = [t for t in tools if t.name == tool_name]

            if len(tool) != 1:
                raise Exception("Tool not found")
            
            # Set reserved arguments
            tool_args["CONVERSATION"] = conversation_history
            tool_args["USER_INPUT"] = user_input

            # Call the tools function with GPT arguments
            tool_response = tool[0].call(tool_args)

            # Some error checking
            if not tool_response: 
                raise Exception("The tool must give a response")
            
            # extend conversation with tool response
            conversation_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_name,
                    "content": tool_response,
                }
            )
        
        # return second response where GPT has acces to the tool call and response
        return ChatGPT.prompt(conversation_history=conversation_history, temperature=0.5, silent=silent)    



if __name__ == "__main__":
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like today? and based on what we've talked about earlier, what is your favorite pet"}
        # {"role": "user", "content": "What will the wind be like from tomorrow morning at 8 to 12 hours later in Bork Havn?"}
        # {"role": "user", "content": "What will the wind be like the in 5 hours from now?"}
        # {"role": "user", "content" : "based on what we've talked about earlier, what is your favorite pet"}
        # {"role": "user", "content" : "search the web to figure out how old dolphins can get"}
    ]
    from ConversationManager import set_global_conversation_manager
    from ToolManager import get_available_tools
    set_global_conversation_manager().conversation = conversation_history
    print(ChatGPT.smart_prompt(conversation_history, tools=get_available_tools(), silent=False))