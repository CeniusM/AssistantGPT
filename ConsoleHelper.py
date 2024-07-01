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

def color(col: str):
    print_checked(col)

def resetColor():
    color(ConsoleColor.RESET)

def print_good(msg: str):
    color(ConsoleColor.OKGREEN)
    print_checked(msg)

def print_error(msg: str):
    color(ConsoleColor.FAIL)
    print_checked(msg)

def print_info(msg: str):
    color(ConsoleColor.OKBLUE)
    print_checked(msg)