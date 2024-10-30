from RSA_Verfahren import RSA_Verfahren
from colorama import Fore, Style
import sys


def argv_check() -> bool:
    if "debug" in sys.argv or "Debug" in sys.argv:
        print(f"{Fore.YELLOW}Debugging Modus aktiviert!{Style.RESET_ALL}")
        Debug = True
    else: Debug = False

    if "lizenz" in sys.argv or "licence" in sys.argv:
        print(f"{Fore.YELLOW}Lizenz Informationen:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}\thttps://github.com/Maix741/RSA_Verfahren{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}\thttps://github.com/Maix741/RSA_Verfahren/blob/main/LICENSE{Style.RESET_ALL}")
    
    return Debug

if __name__ == "__main__":
    try: Debug = argv_check()
    except ImportError: Debug = False
    Programm = RSA_Verfahren(debug=Debug)
    running = True
    while running:
        running = Programm.Get_mode()