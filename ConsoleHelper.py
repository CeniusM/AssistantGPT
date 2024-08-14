class ConsoleColor:
    RESET = '\033[0m'
    ENDC = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

LogEnabled = True

# Only prints if logging is enabled
def print_checked(msg):
    if LogEnabled is True:
        print(msg)
    color(ConsoleColor.RESET)

def color(col: str):
    if LogEnabled is True:
        print(col, end='')

def resetColor():
    color(ConsoleColor.RESET)

def print_good(msg: str):
    color(ConsoleColor.OKGREEN)
    print_checked(msg)

def print_error(msg: str):
    color(ConsoleColor.FAIL)
    print_checked(msg)

def print_info(msg: str):
    color(ConsoleColor.OKCYAN)
    print_checked(msg)

def print_warning(msg: str):
    color(ConsoleColor.WARNING)
    print_checked(msg)

def print_bold(msg: str):
    color(ConsoleColor.UNDERLINE)
    print_checked(msg)


def error_handling(exception: Exception): # take in an exception and print its corresponding message
    #check exception as a string
    if "FileNotFoundError" in str(exception):
        print_error("File not found")
    elif "PermissionError" in str(exception):
        print_error("Permission denied")
    elif "sr.WaitTimeoutError" in str(exception):
        print_error("Listening timed out, no speech detected.")
    elif "sr.UnknownValueError" in str(exception):
        print_error("Speech Recognition could not understand audio")
    elif "sr.RequestError" in str(exception):
        print_error("Could not request results from Google Speech Recognition service")
    elif "OSError" in str(exception):
        print_error("Error: Microphone not found. Please check your microphone connection.")
    elif "TypeError" in str(exception):
        print_error("Error: TypeError")
    else:
        print_error("An unknown error occurred")
    
    print_warning("Error msg: " + str(exception))