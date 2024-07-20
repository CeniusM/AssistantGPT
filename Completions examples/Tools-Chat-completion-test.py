import json
from FileManager import *

chat_completion = {
    "id": "chatcmpl-9laCf8pzvvx4b7GJvhlRtI76tgIgO",
    "choices": [
        {
            "finish_reason": "tool_calls",
            "index": 0,
            "logprobs": None,
            "message": {
                "content": None,
                "role": "assistant",
                "function_call": None,
                "tool_calls": [
                    {
                        "id": "call_GQwAbtS1T05Mtr2kfvNsZ4R6",
                        "function": {
                            "arguments": "{}",
                            "name": "look_through_memory"
                        },
                        "type": "function"
                    }
                ]
            }
        }
    ],
    "created": 1721127609,
    "model": "gpt-3.5-turbo-0125",
    "object": "chat.completion",
    "service_tier": None,
    "system_fingerprint": None,
    "usage": {
        "completion_tokens": 11,
        "prompt_tokens": 358,
        "total_tokens": 369
    }
}

# Convert to JSON
response_json = json.dumps(chat_completion, indent=4)

# Save the JSON string to a file
with open('response.json', 'w') as file:
    file.write(response_json)

# with open('response.json', "r") as file:
#     resres = file.read()

# resr = json.loads(resres)

resr = read_json_file("response.json")
print(resr["usage"]["total_tokens"])

