import speech_recognition as sr
from ConsoleHelper import *
from SmartSpeaker import *

class SmartMic:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        self.adjust_for_ambient_noise()

    def listen(self, threshold=5, timeout=10):

        with self.mic as source:
            print_info("Listening...")
            
            try:
                # Listen for speech until silence
                audio = self.recognizer.listen(source, phrase_time_limit=threshold, timeout=timeout)
                print("Stopped listening, processing audio...")
                return audio
            except sr.WaitTimeoutError:
                print_error("Listening timed out, no speech detected.")
            except sr.UnknownValueError:
                print_error("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print_error(f"Could not request results from Google Speech Recognition service; {e}")
    
    def adjust_for_ambient_noise(self):
        print_info("Adjusting for ambient noise, please wait...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def record_to_file(self, duration):
        pass

    def interpret_speech(self, audio):
        try:
            # Recognize speech using Google Web Speech API
            speech = self.recognizer.recognize_google(audio)
            print_bold("You said: " + speech)
            return speech
        except:
            return None
