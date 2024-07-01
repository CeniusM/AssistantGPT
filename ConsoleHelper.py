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

def color(col: str):
    print(col, end='')

def resetColor():
    color(ConsoleColor.RESET)

def print_good(msg: str):
    color(ConsoleColor.OKGREEN)
    print(msg)

def print_error(msg: str):
    color(ConsoleColor.FAIL)
    print(msg)

def print_info(msg: str):
    color(ConsoleColor.OKBLUE)
    print(msg)