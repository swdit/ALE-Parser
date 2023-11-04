from colorama import Back, Fore
import inspect


clrs = Fore.RESET + Back.RESET
magenta = clrs + Fore.LIGHTMAGENTA_EX
blue = clrs + Fore.BLUE
green = clrs + Fore.LIGHTGREEN_EX
grey =  clrs + Fore.WHITE
yellow =  clrs + Fore.YELLOW
turk = clrs + Fore.LIGHTCYAN_EX
red = clrs + Fore.RED

def printme(vrname): # prints the name, the content and the class of the variable fed into printme
    for var_name, var_value in inspect.currentframe().f_back.f_locals.items():
        if var_value is vrname:
            vartitle = var_name
            break
    else:
        vartitle = "<unknown>"
    vrtype = str(type(vrname))
    vrname = str(vrname)
    print(magenta + vartitle, ": ", green + vrname, turk + vrtype + clrs)