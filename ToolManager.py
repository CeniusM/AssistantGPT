from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *

#this document has been created to solve import error

def get_weather(user_input, parameters=None):
    DMI.create_response(user_input, parameters)

def look_through_memory(user_input):
    Memory.create_response(user_input)

def web_search(user_input):
    WebSearch.create_response(user_input)
    
def adjust_mic():
    SmartMic.adjust_for_ambient_noise()

get_weather("hey")