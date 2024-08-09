import openai

from ConsoleHelper import *
from KeyManager import *
from ToolManager import get_available_tools, get_available_tools_json

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

    def smart_prompt(conversation_history, temperature=0.5, silent=False):
        available_tools =   get_available_tools()
        tools_json =        get_available_tools_json()
        
        response, tool_calls, message = ChatGPT.prompt(
                                        conversation_history=conversation_history,
                                        temperature=temperature,
                                        silent=silent,
                                        tools_json=tools_json,
                                        tool_choice="auto"
                                        )
        
        # check if the model wanted to call a function, if not, return
        if not tool_calls:
           return response
        
        conversation_history.append(message)  # extend conversation with assistant's reply    ¯\_(ツ)_/¯

        # Send the info for each function call and function response to the model
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool = available_tools[tool_name]

            # Use get on args if defined by tool
            tool_args = tool_args if "get" not in tool.keys() else tool_args.get(tool["get"])

            # Call the tools function with arguments if defined by tool
            tool_response = tool["function"](tool_args) if tool["use_args"] else tool["function"]()

            # If tool has predefined response, we just return that
            tool_response = tool_response if "response" not in tool.keys() else tool["response"]

            # Some error checking
            if not tool_response: raise Exception("The tool must give a response")
            
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
        return ChatGPT.prompt(conversation_history=conversation_history, temperature=0.5, silent=False)    



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
    set_global_conversation_manager().conversation = conversation_history
    print(ChatGPT.smart_prompt(conversation_history, silent=False))