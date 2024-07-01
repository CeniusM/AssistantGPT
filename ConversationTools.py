
def check_text_for_exit(text):
    byewords = [" exit", "quit", " goodbye", " farewell"]
    text = " " + text
    if any(word in text for word in byewords):
        return True