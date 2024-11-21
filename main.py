from RSA_Verfahren import RSA_Verfahren
from colorama import Fore, Style
import sys


def argv_check(args: list) -> bool:
    """:return debug: returns True if debugging mode has been activated"""
    if "debug" in args or "Debug" in args:
        print(f"{Fore.YELLOW}Debugging mode activated!{Style.RESET_ALL}")
        debug = True
    else: debug = False

    if "lizenz" in args or "licence" in args:
        print(f"{Fore.YELLOW}Licence information:")
        print(f"\tSource: https://github.com/Maix741/RSA_Verfahren")
        print(f"\tLicence: https://github.com/Maix741/RSA_Verfahren/blob/main/LICENSE\n{Style.RESET_ALL}")

    return debug


if __name__ == "__main__":
    debug: bool = argv_check(sys.argv)
    Programm = RSA_Verfahren(debug=debug)
    running = True
    while running:
        running = Programm.get_mode()