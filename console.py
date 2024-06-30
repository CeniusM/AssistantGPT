class consoleColor:
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

def color(col: str):
    print(col, end='')

def resetColor():
    color(consoleColor.RESET)

def print_good(msg: str):
    color(consoleColor.OKGREEN)
    print(msg)

def print_error(msg: str):
    color(consoleColor.FAIL)
    print(msg)

def print_info(msg: str):
    color(consoleColor.OKBLUE)
    print(msg)