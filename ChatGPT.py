from ConsoleHelper import *
from KeyManager import *
import openai

class ChatGPT:    

    total_cost = 0
    
    def prompt(conversation_history, silent=False):
        openai.api_key = get_GPT_key()

        completion = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages= conversation_history,
                temperature=0.5,
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