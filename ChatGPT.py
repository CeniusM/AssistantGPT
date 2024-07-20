from ConsoleHelper import *
from KeyManager import *
import openai


class ChatGPT:    

    total_cost = 0
    
    def prompt(conversation_history, temperature=0.2):
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
        return response


    def smart_prompt(conversation_history, temperature=0.5, silent=False, debug = False):

        if not debug:
            openai.api_key = get_GPT_key()
            tools = read_json_file("Tools.json")

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

        else:
            completion = read_json_file("Completions examples\\GPT_weather.json")
            tool_calls = completion["choices"][0]["message"]["tool_calls"]
            response = completion["choices"][0]["message"]["content"]

        #too

        if not tool_calls: # check if the model wanted to call a function
            if not silent:
                print_bold(f"\n{response}\n")

            return response
        
        else:
            from ToolManager import get_weather, look_through_memory, web_search, adjust_mic
            # from DMI import create_response
            # from Memory import create_response
            # from WebSearch import create_response
            # from SmartMic import adjust_for_ambient_noise
            # call the function   Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_weather_forecast" : get_weather,
                "look_through_memory" : look_through_memory,
                "web_search" : web_search,
                "adjust_microphone" : adjust_mic
            }

            conversation_history.append(completion.choices[0].message)  # extend conversation with assistant's reply    ¯\_(ツ)_/¯
            
            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                if debug:
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])
                else:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                function_to_call = available_functions[function_name]

                if function_name == "get_weather_forecast":
                    function_response = function_to_call(GPT_parameters = function_args)
                elif function_name == "look_through_memory":
                    function_response = function_to_call()
                elif function_name == "web_search":
                    function_response = function_to_call(search_query = function_args.get("search_query"))                 
                elif function_name == "adjust_microphone": #if no input or output is needed
                    function_to_call()
                    continue

                if debug:
                    conversation_history.append(
                        {
                            "tool_call_id": tool_call["id"],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response

                else:
                    conversation_history.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response


            
            second_response = ChatGPT.prompt(conversation_history=conversation_history, temperature=0.5)
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
    print(ChatGPT.smart_prompt(conversation_history, debug=False))