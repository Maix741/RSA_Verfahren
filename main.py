from RSA_Verfahren import RSA_Verfahren
from colorama import Fore, Style
import sys


def argv_check() -> bool:
    """:return debug: returns True if debugging mode has been activated"""
    if "debug" in sys.argv or "Debug" in sys.argv:
        print(f"{Fore.YELLOW}Debugging mode activated!{Style.RESET_ALL}")
        Debug = True
    else: Debug = False

    if "lizenz" in sys.argv or "licence" in sys.argv:
        print(f"{Fore.YELLOW}Licence information:")
        print(f"\tSource: https://github.com/Maix741/RSA_Verfahren")
        print(f"\tLicence: https://github.com/Maix741/RSA_Verfahren/blob/main/LICENSE\n{Style.RESET_ALL}")

    return Debug


if __name__ == "__main__":
    Debug: bool = argv_check()
    Programm = RSA_Verfahren(debug=Debug)
    running = True
    while running:
        running = Programm.Get_mode()