from DMI import *
from Memory import *
from WebSearch import *
from SmartMic import *

#this document has been created to solve import error

def get_weather(conversation_history, parameters=None):
    DMI.create_response(conversation_history, parameters)

def look_through_memory(conversation_history):
    Memory.create_response(conversation_history)

def web_search(conversation_history):
    WebSearch.create_response(conversation_history)
    
def adjust_mic():
    SmartMic.adjust_for_ambient_noise() #make work with self

