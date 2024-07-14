from FileManager import *
from ConsoleHelper import *
from SmartMic import *
from DMI import *
from Memory import *
from WebSearch import *
from ConversationManager import *



def check_text(text, smart_check=False):

    #check if smart_check and use ChatGPT's function call to check the text
    if smart_check:
        convo = ConversationManager(promptname="smart_check.txt").api_convo_setup(text)
        adjust_mic , web_search, weather_forecast, remember = ChatGPT.check_text(convo, "smart_check.txt")
    
    else:    
        adjust_mic , web_search, weather_forecast, remember = check_text_for_key_words(text)

    #run text commands
    if adjust_mic:
        SmartMic.adjust_for_ambient_noise()
    if web_search:
        text = WebSearch.create_response(text)
    if weather_forecast:
        text = DMI.create_response(text)
    if remember:
        text = Memory.create_response(text)

    return text

def word_in_text(text, words):
    text = " " + text
    words = [" "+word.lower() for word in words]
    return any(word in text for word in words)

def check_text_for_key_words(text):

    #check for all keywords
    adjust_mic =check_text_for_ambient_noise(text)
    web_search = check_text_for_web_search(text)
    weather_forecast = check_text_for_weather(text)
    remember = check_text_for_memory(text)

    return adjust_mic , web_search, weather_forecast, remember

def check_text_for_exit(text):
    #check for exit words
    byewords = ["exit", "quit", "goodbye", "farewell"]
    if word_in_text(text, byewords):
        print_bold("\nGoodbye!\n")
        return True

def check_text_for_ambient_noise(text):
    noise_phrases = ["ambient noise", "background noise", "noise", "støj","støjen", "baggrundsstøj", "baggrundsstøjen" "støjniveau", "støjniveauet", ]
    adjustment_phrases = ["adjust", "update", "change", "calibrate", "correct", "fix", "set", "reset", "kalibrer", "juster", "opdater", "ændre", "ret", "sæt", "nulstil"]
    return word_in_text(text, noise_phrases) and word_in_text(text, adjustment_phrases)


def check_text_for_empty(text):
    if text == " " or text == "":
        print_warning("Did not get what you said (no text)")
        return True
    return False

def check_text_for_weather(text):
    weather_phrases = ["weather", "vejret", "forecast", "prognose", "temperature", "temperatur", "rain", "regn", "wind", "vind", "cloud", "sky", "lightning", "lyn", "snow", "sne", "thunder", "torden", "storm", "tomorrow", "today", "i morgen", "i dag"]
    return word_in_text(text, weather_phrases)


def check_text_for_web_search(text):
    search_phrases = ["search", "google", "look up", "søg", "slå op", "check internet", "check the internet", "check online", "check the web" ]
    return word_in_text(text, search_phrases)

def check_text_for_memory(text):
    memory_phrases = ["memory", "husk", "remember", "recall","genkald", "hukommelse"]
    return word_in_text(text, memory_phrases)


