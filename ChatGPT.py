import openai

from ConsoleHelper import *
from KeyManager import *

from ToolManager import get_available_tools

class ChatGPT:    

    total_cost = 0
    
    def prompt(conversation_history, temperature=0.2, silent=True):
        openai.api_key = get_GPT_key()

        completion = openai.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = conversation_history,
                temperature = temperature
            )
    
        total_tokens = completion.usage.total_tokens
        cost = round((total_tokens*0.002)/1000, 10)
        ChatGPT.total_cost = round(ChatGPT.total_cost + cost, 10)
        
        response = completion.choices[0].message.content
        if not silent:
            print_bold(f"\n{response}\n")
        return response


    def smart_prompt(conversation_history, temperature=0.5, silent=False):
        openai.api_key = get_GPT_key()

        tools = read_json_file("Tools.json")
        available_tools = get_available_tools()


        completion = openai.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = conversation_history,
                temperature = temperature,
                tools = tools,   #all functions
                tool_choice = "auto" #automaticly chose if functions should be called
            )

        total_tokens = completion.usage.total_tokens
        cost = round((total_tokens*0.002)/1000, 10)
        ChatGPT.total_cost = round(ChatGPT.total_cost + cost, 10)
        
        response = completion.choices[0].message.content
        tool_calls = completion.choices[0].message.tool_calls       

        # else:
        #     completion = read_json_file("Completions examples\\GPT_weather.json")
        #     tool_calls = completion["choices"][0]["message"]["tool_calls"]
        #     response = completion["choices"][0]["message"]["content"]

        if not tool_calls: # check if the model wanted to call a function
            if not silent:
                print_bold(f"\n{response}\n")

            return response
        
        else:
            conversation_history.append(completion.choices[0].message)  # extend conversation with assistant's reply    ¯\_(ツ)_/¯
            
            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                tool = available_tools[tool_name]

                # Edge cases for the function args
                if tool_name == "web_search":
                    tool_args = tool_args.get("search_query")

                function_response = tool["function"](tool_args)

                # Edge cases for the function response
                if tool_name == "adjust_microphone":
                    function_response = "Microphone adjusted"
                
                conversation_history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": tool_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            
            second_response = ChatGPT.prompt(conversation_history=conversation_history, temperature=0.5, silent=False)
            return second_response

    
    
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