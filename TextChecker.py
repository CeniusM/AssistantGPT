from FileManager import *
from ConsoleHelper import *
from SmartMic import *
from DMI import *
from Memory import *
from WebSearch import *



def check_text(text):
    
    if check_text_for_ambient_noise(text):
        SmartMic.adjust_for_ambient_noise()
        print_bold("Adjusted for ambient noise")

    #if check_text_for_empty(text):
        #return continue

    if check_text_for_web_search(text):
        print_bold("Searching.")
        #text = WebSearch.create_response(text)


    if check_text_for_weather(text):
        print_bold("Getting weather data")
        text = DMI.create_response(text)

    if check_text_for_memory(text):
        print_bold("Checking memory")
        text = Memory.create_response(text)

    return text


def word_in_text(text, words):
    text = " " + text
    words = [" "+word.lower() for word in words]
    return any(word in text for word in words)



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


