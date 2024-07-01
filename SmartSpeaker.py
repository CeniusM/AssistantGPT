import pygame
import winsound
import os
from google.cloud import texttospeech

class SmartSpeaker:    
#method for finding if the langeuage of the response is danish or english, for the synthesized reader
    def get_language(text):
        #list of danish letters
        danish_letters = ["æ", "ø", "å"]
        danish_letters_set = set(danish_letters)
        #list of danish words
        danish_words = ["hvad", "er", "jeg", "du", "vi", "de", "den", "det", "og", "til", "med", "ikke"]
        danish_words_set = set(danish_words)
        #danish_words = ["af", "fordi", "alle", "fra", "kommer", "fri", "kun", "på", "andre", "få", "kunne", "sagde", "at", "gik", "lang", "se", "blev", "glad", "lidt", "selv", "bliver", "godt", "lige", "sidste", "bort", "ham", "lille", "sig", "da", "han", "løb", "sin", "dag", "hans", "man", "sine", "de", "har", "mange", "skal", "dem", "havde", "med", "skulle", "den", "have", "meget", "små", "der", "hele", "men", "som", "deres", "hen", "mere", "stor", "det", "hende", "mig", "store", "dig", "her", "min", "så", "dog", "hjem", "mod", "tid", "du", "hun", "mon", "til", "efter", "hvad", "må", "tog", "eller", "hver", "ned", "ud", "en", "hvis", "nej", "under", "end", "hvor",    "noget", "var", "er", "igen", "nok", "ved", "et", "ikke", "nu", "vi",    "far", "ind", "når", "vil", "fik", "jeg", "og", "ville", "fin", "for", "forbi", "kan"]

        #take set og the response
        letterset = set(text)
        #if the response contains any of these letters, it is danish
        if len(letterset.intersection(danish_letters_set)) > 0:
            return "da-DK"
        
        #take set of the words in the response
        wordset = set(text.split()) 
        #if the response contains any of these words, it is danish
        if len(wordset.intersection(danish_words_set)) > 0:
            return "da-DK"
        
        return "en-US" 



    def create_audio_file(audio_path, audio_file):
        with open(audio_path, "wb") as output:
            # Write the response to the output file.
            output.write(audio_file)



    def play(audio_file):
        pygame.mixer.init()                     # initialize the pygame mixer module
        pygame.mixer.music.load(audio_file)     # load the audio file
        
        pygame.mixer.music.play()               # play the audio file
        while pygame.mixer.music.get_busy():    # wait for the audio to finish playing
            pygame.time.Clock().tick(10)        # wait for 10 milliseconds to not hog CPU time 

        pygame.mixer.quit()                     # quit the mixer

    def beep(Hz=440, milliseconds=500):
        winsound.Beep(Hz, milliseconds) # Beep to let you know it reset # Hz , milliseconds

    def generate_speech(text, lang, male = True):

        # Imports the Google Cloud client library
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "Keys\\google_key.json"
        
        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        #Set the language of the response
        language_response = SmartSpeaker.get_language(text)

        # Build the voice request, select the language with get_language and the ssml_gender
        # voice name depending on language and male boolean
        if male == True:
            if language_response == "en-US":
                voice_name = "en-US-Neural2-I" #English Male
            elif language_response == "da-DK":
                voice_name = "da-DK-Wavenet-C" #Danish Male
            tts_gender = texttospeech.SsmlVoiceGender.MALE
            
        else:
            if language_response == "en-US":
                voice_name = "en-US-Neural2-E" #English Female
            elif language_response == "da-DK":
                voice_name = "da-DK-Neural2-D" #Danish Female
            tts_gender = texttospeech.SsmlVoiceGender.FEMALE

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_response, name=voice_name, ssml_gender=tts_gender
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MULAW
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content

    def play_voice(text):
        lang = SmartSpeaker.get_language(text)
        
        audio_content = SmartSpeaker.generate_speech(text, lang)

        audio_path = "Audiofiles\\tempAudio.wav"

        SmartSpeaker.create_audio_file(audio_path, audio_content)

        SmartSpeaker.play(audio_path)

if __name__ == "__main__":
    
    text ="Oh, you're looking for a list of organelles found in a cell? Do you want me to list them all or are you looking for specific ones?"
    SmartSpeaker.play_voice(text)
 


