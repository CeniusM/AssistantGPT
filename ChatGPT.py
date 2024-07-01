from KeyManager import *
import openai

class ChatGPT:    
    def prompt(conversation_history):
        openai.api_key = get_GPT_key()

        completion = openai.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages= conversation_history,
                temperature=0.5,
                presence_penalty=0.5,
                frequency_penalty=0.5,
            )
        
        response = completion.choices[0].message.content

        print(f"\n{response}\n")

        return response