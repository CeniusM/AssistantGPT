from ConsoleHelper import *
from KeyManager import *
import openai

class ChatGPT:    

    total_cost = 0
    
    def prompt(conversation_history, temperature=0.6, silent=False):
        openai.api_key = get_GPT_key()
        temperature = temperature

        completion = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages= conversation_history,
                temperature=temperature,
                presence_penalty=0.5,
                frequency_penalty=0.5,
            )
        
        response = completion.choices[0].message.content
        if not silent:
            print_bold(f"\n{response}\n")
    
        total_tokens = completion.usage.total_tokens
        cost = round((total_tokens*0.002)/1000, 10)
        ChatGPT.total_cost = round(ChatGPT.total_cost + cost, 10)

        return response
    

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
    ChatGPT.prompt(conversation_history)