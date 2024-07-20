from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *

#this document has been created to solve import error

def get_weather(GPT_parameters):
    DMI.create_response(GPT_parameters)

def look_through_memory():
    Memory.create_response()

def web_search(search_query):
    WebSearch.create_response(search_query=search_query)
    
def adjust_mic():
    SmartMic.adjust_for_ambient_noise() #make work with

