from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *

#this document has been created to solve import error

def get_weather(GPT_parameters):
    return DMI.create_response(GPT_parameters)


def look_through_memory():
    return Memory.create_response()

def web_search(search_query):
    return WebSearch.create_response(search_query=search_query)
    
def adjust_mic():
    SmartMic().adjust_for_ambient_noise()

