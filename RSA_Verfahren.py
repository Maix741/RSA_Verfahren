from RSA_Key_generate import Generate_Keys
from RSA_Key_split import Split_Keys
from colorama import Fore, Style
from tkinter import filedialog
from tqdm import tqdm
import os, sys
import time


class RSA_Verfahren:
    """Class for encrypting and decrypting with RSA \n
    The object needs to be initialized\n
    :param bool dialog: imediadly open filedialog for choosing Key file standart is False
    :param int FileThreshhold: lenght threshhold for writing en- or decryted text in a File (int)
    :param str forcefilecreation_keyword: Keyword that if it is at the beginning of the inputs a file will always be created
    :param bool debug: Enable debug mode for viewing nessesary time for en- and decrypting
    :return None:"""
    def __init__(self,
                 dialog: bool = False, FileThreshhold: int = 200, forcefilecreation_keyword: str = "/DateiEr", debug: bool = False
                ) -> None:
        self.debug: bool = debug
        self.fileThreshhold: int = FileThreshhold # set object variables
        self.forceFilecreationKeyword: str = forcefilecreation_keyword
        self.reset_modes()
        print(self.options)

        self.D, self.E, self.n = self.load_key(dialog) # load the Key


    def fix_modes(self) -> None: #TODO: remove this
        """Temporary fix for Problem: selectedMode not in self.modes -> line 66"""
        self.modes = [mode.lower() for mode in self.modes] # makes all modes lowercase


    def reset_modes(self) -> None:
        self.modes = [
            "Ver", "Ent", "Ver Datei", "Ent Datei",                        # RSA shortend (0-3)
            "Verschlüsseln", "Entschlüsseln",                              # RSA full (4-5)
            "Sch Generieren", "Sch teilen", "Sch auswählen", "tauschen",   # RSA extra (6-9)
            "Modi", "clear"                                                # RSA Quality of Life (10)
            ]
        self.options = f"""Verfügbare Optionen:
        1. Verschlüsseln -> "{self.modes[0]}", "{self.modes[4]}", "{self.modes[2]}"
        2. Entschlüsseln -> "{self.modes[1]}", "{self.modes[5]}", "{self.modes[3]}"
        3. Neue Schlüsselpaare generieren -> "{self.modes[6]}"
        4. Schlüssel aufteilen -> "{self.modes[7]}"
        5. Schlüsseldatei neu auswählen -> "{self.modes[8]}"
        6. Schlüssel tauschen -> "{self.modes[9]}"
        7. Diese Liste anzeigen -> "{self.modes[10]}"
        8. Konsole leeren -> "{self.modes[11]}"
        Speicherung in eine Datei zwingen -> "{self.forceFilecreationKeyword}" am Anfang des Textes oder der Liste\n"""

        self.fix_modes()


    def get_mode(self) -> bool:
        """Method for choosing RSA mode from user input \n
        :return bool: returns False when the user wnts to quit else: True"""
        selectedMode = input('Modus(oder "quit"): ').lower().strip().replace("_", " ")

        # check if Mode is valid or quit
        if selectedMode == "q" or selectedMode == "quit":
            return False

        if selectedMode == "read-keys" and self.debug:
            print({"D": self.D, "E": self.E, "n": self.n})

        if selectedMode not in self.modes or selectedMode == "n/a":
            print(f"{Fore.RED}Ungültiger selectedMode!{Style.RESET_ALL}")
            return True


        # ver, verschlüsseln | ver_datei
        if selectedMode == self.modes[0] or selectedMode == self.modes[4]:
            encryptedText, timeNessesary = self.encrypt_text()
            if encryptedText:
                print(f"\n{encryptedText}\n") # TODO: Do more with text
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum encrypt: {timeNessesary}{Style.RESET_ALL}")

        elif selectedMode == self.modes[2]:
            encryptedText, timeNessesary = self.encrypt_file()
            if encryptedText:
                print(f"\n{encryptedText}\n") # TODO: Do more with text
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum encrypt: {timeNessesary}{Style.RESET_ALL}")


        # ent, entschlüsseln | ent_datei
        if selectedMode == self.modes[1] or selectedMode == self.modes[5]:
            decryptedText, timeNessesary = self.decrypt_text()
            if decryptedText:
                print(f"\n{decryptedText}\n")# TODO: Do more with text
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum encrypt: {timeNessesary}{Style.RESET_ALL}")

        elif selectedMode == self.modes[3]:
            decryptedText, timeNessesary = self.decrypt_file()
            if decryptedText:
                print(f"\n{decryptedText}\n")# TODO: Do more with text
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum encrypt: {timeNessesary}{Style.RESET_ALL}")


        # generate_keys
        if selectedMode == self.modes[6]:
            Generator = Generate_Keys()
            p, q, self.n, self.E, self.D = Generator.generate_keys()
            if input("Datei erstellen(y/n): ").lower() == "y":
                Generator.write_Keys((p, q, self.n, self.E, self.D))

        # split_keys
        elif selectedMode == self.modes[7]:
            Split_Keys().create_Public_Private((self.D, self.E, self.n))
            print(f"{Fore.GREEN}Schlüssel erfolgreich aufgeteilt{Style.RESET_ALL}")

        # choose_key
        elif selectedMode == self.modes[8]:
            self.D, self.E, self.n = self.load_key(True)
            print(f"{Fore.GREEN}Schlüssel wurde erfolgreich geladen!{Style.RESET_ALL}")

        # swap keys
        elif selectedMode == self.modes[9]:
            self.D, self.E = self.E, self.D
            print(f"{Fore.GREEN}Schlüssel wurde erfolgreich getauscht{Style.RESET_ALL}")

        # print options/modes
        elif selectedMode == self.modes[10]:
            print(self.options)

        # clear
        elif selectedMode == self.modes[11]:
            print("\033[H\033[J", end="")
            print(self.options)


        return True


    def en_or_decrypt(self, text: int, key: int, n: int) -> int:
        """Method for encrypting and decrypting with RSA\n
        :param int text: ASCII of a character (int)
        :param int Schlüssel: RSA Key (ether D or E) (int)\n
        :param int n: RSA Key fragment n (int)\n
        :return int: encrypted or decrypted text"""
        return pow(text, key, n)


    def load_key(self, dialog: bool = False) -> tuple[int]:
        """Method for loading all nessacary Key Fragments\n
        :param bool dialog: if True the path to the Key file will be choosen with a filedialog
        :return tuple: Key fragments D, E, n"""
        currentDirectory = os.path.dirname(sys.argv[0])
        file: str = os.path.join(currentDirectory, "KEYS", "RSA_Key.key")
        if dialog:
            file = filedialog.askopenfilename(initialdir=currentDirectory, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, n, e, d = Generator.generate_keys()
                    if input("Datei erstellen?(y/n): ").lower().strip() == "n": # TODO: less nesting
                        return (d, e, n)
                    file = Generator.write_Keys((p, q, n, e, d))
                else: file = os.path.join(currentDirectory, "KEYS", "RSA_Key.key")

        keys: list[int] = []
        try:
            with open(file, "r") as keyFile:
                keys = keyFile.read().splitlines()[:5]
                keyFile.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Schlüsseldatei: {file}{Style.RESET_ALL}")
            return self.load_key(True)


        # Test Key
        if not self.test_key((keys[:5])):
            print(f"{Fore.RED}Ungültiger Schlüssel oder Ungültige Schlüsseldatei!{Style.RESET_ALL}")
            return self.load_key(True)

        # return D, E, n
        return (keys.pop(4), keys.pop(3), keys.pop(2))


    def only_public_test(self, key: tuple[int | str]) -> bool:
        for k in key[2:4]:
            if k and k.isdigit():
                continue

            return False

        self.reset_modes()
        self.modes[1], self.modes[5], self.modes[3], self.modes[7], self.modes[9] = "n/a", "n/a", "n/a", "n/a", "n/a"
        print("\033[H\033[J", end="")
        print(self.options)

        if self.debug:
            print(f"{Fore.GREEN}Öffentliche Schlüsseldatei gültig{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}Nur öffentlicher Schlüssel geladen{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}decrypt wird deaktiviert{Style.RESET_ALL}")
        return True


    def load_big_key(self, setTo: int = 1000000000) -> None:
        """edits sys.setrecursionlimit and sys.set_int_max_str_digits to a default of 1000000000\n
        :return None:"""
        print(f"{Fore.RED}Schlüssel zu groß!{Style.RESET_ALL}")
        print(f"{Fore.RED}Schalte um auf große Schlüssel!{Style.RESET_ALL}")
        if self.debug:
            print(f"{Fore.YELLOW}sys variablen werden geändert...{Style.RESET_ALL}""")
        sys.setrecursionlimit(setTo)
        sys.set_int_max_str_digits(setTo)
        print(f"{Fore.RED}Schlüsselauswahl bitte neu versuchen!{Style.RESET_ALL}")


    def only_private_test(self, key: tuple[int | str]) -> bool:
        for k in key[2:4]:
            if k and k.isdigit():
                continue

            return False

        self.reset_modes()
        self.modes[0], self.modes[4], self.modes[2], self.modes[7], self.modes[9] = "n/a", "n/a", "n/a", "n/a", "n/a"
        print("\033[H\033[J", end="")
        print(self.options)

        if self.debug:
            print(f"{Fore.GREEN}Private Schlüsseldatei gültig{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}Nur privater Schlüssel geladen{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Verchlüsseln wird deaktiviert{Style.RESET_ALL}")
        return True


    def test_key(self, key: tuple[int | str]) -> bool:
        """Method for testing a RSA Key\n
        Tests if the key is a number and\n
        if de and encrypting works\n
        :param key tuple: The Key as a tuple
        :return validKey bool: returns True if the Key is valid"""
        if key[0] == "Mode: Public": return self.only_public_test(key)
        if key[0] == "Mode: Private": return self.only_private_test(key)
        else:
            self.reset_modes()

        for k in key[2:5]:
            if k and k.isdigit():
                continue

            return False

        try:
            startTest = time.time()
            _, _, n, e, d = key
            testText = chr(255)
            entText = 255
            verText = self.en_or_decrypt(ord(testText), int(e), int(n))
            entText = self.en_or_decrypt(verText, int(d), int(n))
            if entText != ord(testText):
                return False

            if self.debug:
                print(f"{Fore.GREEN}Schlüsseldatei gültig{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Testzeit war: {time.time() - startTest}{Style.RESET_ALL}")
            return True

        except ValueError:
            self.load_big_key()
            return False


    def get_text(self) -> str:
        """Method for returning encryptable text that is compatable with the encryption method\n
        :return str: text that would not create an Error"""
        text = input('Zu verschlüsselnder Text(oder "quit"): ')
        forcefile = False
        if not text:
            print(f'{Fore.RED}Bitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu kehren{Style.RESET_ALL}')
            return self.get_text()

        if text.lower() == "quit":
            return None, False

        for letter in text:
            if ord(letter) < int(self.n):
                continue

            print(f"{Fore.RED}Ascii der Buchstaben darf nicht größer als {self.n} sein!{Style.RESET_ALL}")
            return self.get_text()

        if text.startswith(self.forceFilecreationKeyword):
            text = text.lstrip(self.forceFilecreationKeyword)
            forcefile = True

        return text, forcefile


    def get_text_decrypt(self) -> list[int]:
        """Method for returning decryptable text that is compatable with the decryption method\n
        :return list: The list of numbers that would be decrypted"""
        text = input('Text(Liste) oder "quit": ').replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        forcefile = False

        if text.lower() == "quit":
            return None, False

        if not text:
            print(f'{Fore.RED}Bitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu kehren{Style.RESET_ALL}')
            return self.get_text_decrypt()

        if text.startswith(self.forceFilecreationKeyword):
            text = text.lstrip(self.forceFilecreationKeyword)
            forcefile = True

        text = text.split(",")
        for Zahl in text:
            if Zahl.isdigit():
                if int(Zahl) < int(self.n):
                    continue

            print(f"{Fore.RED}Eingabe muss eine Liste von ganzen Zahlen unter {self.n} sein!{Style.RESET_ALL}")
            return self.get_text_decrypt()

        return text, forcefile


    def encrypt(self, text: str) -> list[int]:
        """Takes a text as a paramatar and returns the encryption of that text\n
        :param str text: The text that will be encrypted
        :return list: The encrypted text in the form of a list"""
        NeuText: list[int] = []
        try:
            for letter in tqdm(text, leave=False):
                NeuText.append(self.en_or_decrypt(ord(letter), int(self.E), int(self.n)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}Verschlüsselung abgebrochen{Style.RESET_ALL}")
            print(f"{Fore.RED}Momentaner Vortschritt zurückgegeben{Style.RESET_ALL}")
            return NeuText

        return NeuText


    def decrypt(self, text: list[int]) -> str:
        """Takes a text as a paramatar and returns the decryption of that text\n
        :param list text: The text that will be decrypted
        :return str: The encrypted text in the form of a string"""
        neutext: str = ""
        try:
            for Zahl in tqdm(text, leave=False):
                neutext += chr(self.en_or_decrypt(int(Zahl), int(self.D), int(self.n)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}Entschlüsselung abgebrochen{Style.RESET_ALL}")
            print(f"{Fore.RED}Momentaner Vortschritt zurückgegeben{Style.RESET_ALL}")
            return neutext

        except Exception:
            return f"{Fore.RED}Liste oder Schlüssel ungültig{Style.RESET_ALL}"

        return neutext


    def encrypt_text(self) -> list[int]:
        """Method for encrypting a inputted text with the Public Key of the RSA method\n
        :return list: The encrypted text in the form of a list
        :return float: Time nessasary for the encryption"""
        text, forcefile = self.get_text()
        startTime = time.time()
        if not text and not forcefile:
            return None, 0.0

        neutext = self.encrypt(text)
        timeNessesary = time.time() - startTime

        return self.check_file_creation(neutext, timeNessesary, forcefile, "Ver")


    def encrypt_file(self) -> list[int]:
        """Method for encrypting a text from a choosen file\n
        :return list: The encrypted text as a list
        :return float: Time nessasary for the encryption"""
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startTime = time.time()
        forcefile = False
        try:
            with open(file, "r") as FileToEncrypt:
                text = FileToEncrypt.read()
                FileToEncrypt.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.encrypt_file()

        if not text:
            print(f"{Fore.RED}Die Datei hat keinen verschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.encrypt_file()

        elif text.startswith(self.forceFilecreationKeyword):
            text = text.lstrip(self.forceFilecreationKeyword)
            forcefile = True

        neutext = self.encrypt(text)
        timeNessesary = time.time() - startTime

        return self.check_file_creation(neutext, timeNessesary, forcefile, "Ver")


    def decrypt_text(self) -> str:
        """Method for decrypting a text\n
        :return str: The decrypted text as a string
        :return float: Time nessasary for the decryption"""
        text, forcefile = self.get_text_decrypt()
        startTime = time.time()

        if not text and not forcefile:
            return None, 0.0

        neutext = self.decrypt(text)
        timeNessesary = time.time() - startTime

        return self.check_file_creation(neutext, timeNessesary, forcefile, "Ent")


    def decrypt_file(self) -> str:
        """Method for decrypting a text from a File\n
        :return str: The decrypted text as a string
        :return float: Time nessasary for the decryption"""
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startTime = time.time()
        forcefile: bool = False
        try:
            with open(file, "r") as FileToDecrypt:
                text = FileToDecrypt.read()
                FileToDecrypt.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.decrypt_file()

        if not text:
            print(f"{Fore.RED}Die Datei hat keinen entschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.decrypt_file()

        if text.startswith(self.forceFilecreationKeyword):
            text = text.lstrip(self.forceFilecreationKeyword)
            forcefile = True

        text = text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
        for Zahl in text:
            if Zahl.isdigit() and int(Zahl) < int(self.n):
                continue

            print(f"{Fore.RED}Ungültige Liste in der Datei! Richtig wäre z.B.: [400, 200]{Style.RESET_ALL}")
            return self.decrypt_file()

        NeuText: str = self.decrypt(text)
        timeNessesary = time.time() - startTime

        return self.check_file_creation(NeuText, timeNessesary, forcefile, "Ent")


    def save_output_in_file(self, text: str, Art: str = "RSA") -> None:
        """Method for saving an de or encrypted text in a .txt file\n
        :param str text: The text that will be written into the file (str)
        :param str Art: (Optional)defines if the file contains en or decrypted text default is "RSA"
        :return None:"""
        dateiName = f"{Art}schlüsselter Output.txt"
        currentDir = os.path.dirname(sys.argv[0])
        file = os.path.join(currentDir, dateiName)
        i = 1
        while os.path.isfile(file):
            file = os.path.join(currentDir, f"{Art}schlüsselter Output{i}.txt")
            i += 1
        with open(file, "w") as Output_File:
            Output_File.write(text)
            Output_File.close()


    def check_file_creation(self, neuText, timeNessesary, forceFile: bool, art: str = "RSA") -> str:
        if not len(str(neuText)) >= self.fileThreshhold and not forceFile:
            return neuText, timeNessesary

        if len(str(neuText)) >= self.fileThreshhold ** 2 or input("Text in einer Datei speichern?(y/n): ") == "y":
            self.save_output_in_file(str(neuText), art)
            return f"{Fore.GREEN}Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!{Style.RESET_ALL}", timeNessesary

        return neuText, timeNessesary


if __name__ == "__main__":
    try:
        from main import argv_check
        debug = argv_check(sys.argv)
    except ImportError: debug = False

    Programm = RSA_Verfahren(debug=debug)
    running = True
    while running:
        running = Programm.get_mode()