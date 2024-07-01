
def check_text_for_exit(text):
    byewords = [" exit", "quit", " goodbye", " farewell"]
    text = " " + text
    if any(word in text for word in byewords):
        return True

#method for finding if the langeuage of the response is danish or english, for the synthesized reader
def get_text_language(text):
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