from ConsoleHelper import *
from KeyManager import *
import openai


class ChatGPT:    

    total_cost = 0
    
    def prompt(conversation_history):
        openai.api_key = get_GPT_key()

        completion = openai.chat.completions.create(
                model = "gpt-3.5-turbo-0125",
                messages = conversation_history,
                temperature = 0.2
            )
    
        total_tokens = completion.usage.total_tokens
        cost = round((total_tokens*0.002)/1000, 10)
        ChatGPT.total_cost = round(ChatGPT.total_cost + cost, 10)
        
        response = completion.choices[0].message.content
        return response


    def smart_prompt(conversation_history, user_input, temperature=0.6, silent=False):
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

        if not tool_calls: # check if the model wanted to call a function
            if not silent:
                print_bold(f"\n{response}\n")

            return response
        
        else:
            from ToolManager import get_weather, look_through_memory, web_search, adjust_mic
            from DMI import create_response
            from Memory import create_response
            from WebSearch import create_response
            from SmartMic import adjust_for_ambient_noise
            # call the function   Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_weather_forecast" : get_weather,
                "look_through_memory" : look_through_memory,
                "web_search" : web_search,
                "adjust_microphone" : adjust_mic
            }
            conversation_history.append(response)  # extend conversation with assistant's reply
            # send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "get_weather":
                    function_response = function_to_call(
                        convo = conversation_history,
                        location = function_args.get("location"),
                        rain = function_args.get("rain"),
                        temperature = function_args.get("temperature"),
                        wind_speed = function_args.get("wind_speed" ),
                        wind_dir = function_args.get("wind_direction" ),
                        snow = function_args.get("snow"),
                        lightning = function_args.get("lightning"),
                        day = function_args.get("day"),
                        time_interval = function_args.get("time_interval"),
                        time_of_day = function_args.get("time_of_day")
                        )
                elif function_name == look_through_memory:
                    function_response == function_to_call(conversation_history = conversation_history)
                elif function_name == web_search:
                    function_response = function_to_call(
                        search_query=function_args.get("search_query"),
                        convo=conversation_history
                        )                 
                else: #if no input is needed
                    function_name()
                    continue

            
                function_data = function_response

                conversation_history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_data,
                    }
                )  # extend conversation with function response
            second_response = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=conversation_history,
                tool_choice="none"
            )  # get a new response from the model where it can see the function response
            return second_response
    

    def check_text(convo):
        #create parameters and make api call
        response = ChatGPT.prompt(convo, silent=True)
        
        adjust_mic = "adjust_mic" in response
        web_search = "web_search" in response
        weather_forecast = "weather_forecast" in response
        remember = "remember" in response

        return adjust_mic, web_search, weather_forecast, remember
    
if __name__ == "__main__":
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like today?"}
    ]
    ChatGPT.smart_prompt(conversation_history)