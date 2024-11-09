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
    :param int FileThreshhold: lenght threshhold for writing en- or decryted Text in a File (int)
    :param str forcefilecreation_keyword: Keyword that if it is at the beginning of the inputs a file will always be created
    :param bool debug: Enable debug mode for viewing nessesary time for en- and decrypting
    :return None:"""
    def __init__(self,
                 dialog: bool = False, FileThreshhold: int = 200, forcefilecreation_keyword: str = "/DateiEr", debug: bool = False
                ) -> None:
        self.modes = [
            "Ver", "Ent", "Ver Datei", "Ent Datei",                        # RSA Richtig (Abkürzungen) (0-3)
            "Verschlüsseln", "Entschlüsseln",                              # RSA Richtig (4-5)
            "Sch Generieren", "Sch teilen", "Sch auswählen", "tauschen",   # RSA Zusatz  (6-9)
            "Modi", "clear"                                                # RSA Quality of Life (10)
            ]
        self.Optionen = f"""Verfügbare Optionen:
        1. Verschlüsseln -> "{self.modes[0]}", "{self.modes[4]}", "{self.modes[2]}"
        2. Entschlüsseln -> "{self.modes[1]}", "{self.modes[5]}", "{self.modes[3]}"
        3. Neue Schlüsselpaare generieren -> "{self.modes[6]}"
        4. Schlüssel aufteilen -> "{self.modes[7]}"
        5. Schlüsseldatei neu auswählen -> "{self.modes[8]}"
        6. Schlüssel tauschen -> "{self.modes[9]}"
        7. Diese Liste anzeigen -> "{self.modes[10]}"
        8. Konsole leeren -> "{self.modes[11]}"
        Speicherung in eine Datei zwingen -> "{forcefilecreation_keyword}" am Anfang des Textes oder der Liste\n"""
        print(self.Optionen)

        self.debug: bool = debug
        self.FileThreshhold: int = FileThreshhold # set object variables
        self.forcefilecreation_keyword: str = forcefilecreation_keyword

        self.D, self.E, self.n = self.load_key(dialog) # load the Key


    def fix_modes(self) -> None:
        """Temporary fix for Problem: Modus not in self.modes -> line 66"""
        self.modes = [mode.lower() for mode in self.modes] # makes all modes lowercase


    def Get_mode(self) -> bool:
        """Method for choosing RSA mode from user input \n
        :return bool: returns False when the user wnts to quit else: True"""
        Modus = input('Modus(oder "quit"): ').lower().strip().replace("_", " ")

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus == "read-keys" and self.debug:
            print({"D": self.D, "E": self.E, "n": self.n})

        elif Modus not in self.modes or Modus == "n/a":
            print(f"{Fore.RED}Ungültiger Modus!{Style.RESET_ALL}")
            return True


        # ver, verschlüsseln | ver_datei
        if Modus == self.modes[0] or Modus == self.modes[4]:
            VerText, zeit = self.verschlüsseln_Text()
            if VerText:
                print(f"\n{VerText}\n") # TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")

        elif Modus == self.modes[2]:
            VerText, zeit = self.Verschlüsseln_Datei()
            if VerText:
                print(f"\n{VerText}\n") # TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")


        # ent, entschlüsseln | ent_datei
        if Modus == self.modes[1] or Modus == self.modes[5]:
            EntText, zeit = self.Entschlüsseln_Text()
            if EntText:
                print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")

        elif Modus == self.modes[3]:
            EntText, zeit = self.Entschlüsseln_Datei()
            if EntText:
                print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.YELLOW}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")


        # generate_keys
        if Modus == self.modes[6]:
            Generator = Generate_Keys()
            p, q, self.n, self.E, self.D = Generator.generate_keys()
            if input("Datei erstellen(y/n): ") == "y":
                Generator.write_Keys((p, q, self.n, self.E, self.D))

        # split_keys
        elif Modus == self.modes[7]:
            Split_Keys().create_Public_Private((self.D, self.E, self.n))
            print(f"{Fore.GREEN}Schlüssel erfolgreich aufgeteilt{Style.RESET_ALL}")

        # choose_key
        elif Modus == self.modes[8]:
            self.D, self.E, self.n = self.load_key(True)
            print(f"{Fore.GREEN}Schlüssel wurde erfolgreich geladen!{Style.RESET_ALL}")

        # swap Keys
        elif Modus == self.modes[9]:
            self.D, self.E = self.E, self.D
            print(f"{Fore.GREEN}Schlüssel wurde erfolgreich getauscht{Style.RESET_ALL}")

        # print options/modes
        elif Modus == self.modes[10]:
            print(self.Optionen)

        # clear
        elif Modus == self.modes[11]:
            print("\033[H\033[J", end="")
            print(self.Optionen)


        return True


    def Ver_oder_Entschlüsseln(self, Text: int, Schlüssel: int, n: int) -> int:
        """Method for encrypting and decrypting with RSA\n
        :param int Text: ASCII of a character (int)
        :param int Schlüssel: RSA Key (ether D or E) (int)\n
        :param int n: RSA Key fragment n (int)\n
        :return int: encrypted or decrypted Text"""
        return pow(Text, Schlüssel, n)


    def load_key(self, dialog: bool = False) -> tuple[int]:
        """Method for loading all nessacary Key Fragments\n
        :param bool dialog: if True the path to the Key file will be choosen with a filedialog
        :return tuple: Key fragments D, E, n"""
        currentdirectory = os.path.dirname(sys.argv[0])
        file: str = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")
        if dialog:
            file = filedialog.askopenfilename(initialdir=currentdirectory, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, n, e, d = Generator.generate_keys()
                    if input("Datei erstellen?(y/n): ").lower().strip() == "n":
                        return (d, e, n)
                    file = Generator.write_Keys((p, q, n, e, d))
                else: file = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")

        Keys: list[int] = []
        try:
            with open(file, "r") as Key_file:
                Keys = Key_file.read().splitlines()[:5]
                Key_file.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.load_key(True)


        # Test Key
        if not self.test_key((Keys[:5])):
            print(f"{Fore.RED}Ungültiger Schlüssel oder Ungültige Schlüsseldatei!{Style.RESET_ALL}")
            return self.load_key(True)

        # return D, E, n
        return (Keys.pop(4), Keys.pop(3), Keys.pop(2))


    def only_public(self, key) -> bool:
        for k in key[2:4]:
            if k and k.isdigit():
                continue

            return False

        self.modes[1], self.modes[5], self.modes[3], self.modes[7], self.modes[9] = "n/a", "n/a", "n/a", "n/a", "n/a"
        self.modes[0], self.modes[4], self.modes[2] = "ver", "verschlüsseln", "ver datei"
        print("\033[H\033[J", end="")
        print(self.Optionen)

        if self.debug:
            print(f"{Fore.GREEN}Private Schlüsseldatei gültig{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}Nur öffentlicher Schlüssel geladen{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Entschlüsseln wird deaktiviert{Style.RESET_ALL}")
        return True


    def only_private(self, key) -> bool:
        for k in key[2:4]:
            if k and k.isdigit():
                continue

            return False

        self.modes[0], self.modes[4], self.modes[2], self.modes[7], self.modes[9] = "n/a", "n/a", "n/a", "n/a", "n/a"
        self.modes[1], self.modes[5], self.modes[3] = "ent", "entschlüsseln", "ent datei"
        print("\033[H\033[J", end="")
        print(self.Optionen)

        if self.debug:
            print(f"{Fore.GREEN}Private Schlüsseldatei gültig{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}Nur privater Schlüssel geladen{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Verchlüsseln wird deaktiviert{Style.RESET_ALL}")
        return True


    def test_key(self, key: tuple[int]) -> bool:
        """Method for testing a RSA Key\n
        Tests if the key is a number and\n
        if de and encrypting works\n
        :param key tuple: The Key as a tuple
        :return validKey bool: returns True if the Key is valid"""
        if key[0] == "Mode: Public": return self.only_public(key)
        if key[0] == "Mode: Private": return self.only_private(key)
        else:
            self.modes = [
            "Ver", "Ent", "Ver Datei", "Ent Datei",                        # RSA Richtig (Abkürzungen) (0-3)
            "Verschlüsseln", "Entschlüsseln",                              # RSA Richtig (4-5)
            "Sch Generieren", "Sch teilen", "Sch auswählen", "tauschen",   # RSA Zusatz  (6-9)
            "Modi", "clear"                                                # RSA Quality of Life (10)
            ]
            self.fix_modes() # FIXME: Make this unnessesary

        for k in key[2:5]:
            if k and k.isdigit():
                continue

            return False

        _, _, n, e, d = key
        testText = chr(255)
        verText = self.Ver_oder_Entschlüsseln(ord(testText), int(e), int(n))
        entText = self.Ver_oder_Entschlüsseln(verText, int(d), int(n))
        if entText != ord(testText):
            return False

        if self.debug:
            print(f"{Fore.GREEN}Schlüsseldatei gültig{Style.RESET_ALL}")

        return True


    def get_Text(self) -> str:
        """Method for returning encryptable Text that is compatable with the encryption method\n
        :return str: Text that would not create an Error"""
        Text = input('Zu verschlüsselnder Text(oder "quit"): ')
        forcefile = False
        if not Text:
            print(f'{Fore.RED}Bitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu kehren{Style.RESET_ALL}')
            return self.get_Text()

        if Text.lower() == "quit":
            return None, False

        for Buchstabe in Text:
            if ord(Buchstabe) < int(self.n):
                continue

            print(f"{Fore.RED}Ascii der Buchstaben darf nicht größer als {self.n} sein!{Style.RESET_ALL}")
            return self.get_Text()

        if Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        return Text, forcefile


    def get_Text_Ent(self) -> list[int]:
        """Method for returning decryptable Text that is compatable with the decryption method\n
        :return list: The list of numbers that would be decrypted"""
        Text = input('Text(Liste) oder "quit": ').replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        forcefile = False

        if Text.lower() == "quit":
            return None, False

        if not Text:
            print(f'{Fore.RED}Bitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu kehren{Style.RESET_ALL}')
            return self.get_Text_Ent()

        if Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        Text = Text.split(",")
        for Zahl in Text:
            if Zahl.isdigit():
                if int(Zahl) < int(self.n):
                    continue

            print(f"{Fore.RED}Eingabe muss eine Liste von ganzen Zahlen unter {self.n} sein!{Style.RESET_ALL}")
            return self.get_Text_Ent()

        return Text, forcefile


    def Verschlüsseln(self, Text: str) -> list[int]:
        """Takes a Text as a paramatar and returns the encryption of that text\n
        :param str Text: The text that will be encrypted
        :return list: The encrypted Text in the form of a list"""
        NeuText: list[int] = []
        try:
            for Buchstabe in tqdm(Text, leave=False):
                NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}Verschlüsselung abgebrochen{Style.RESET_ALL}")
            print(f"{Fore.RED}Momentaner Vortschritt zurückgegeben{Style.RESET_ALL}")
            return NeuText

        return NeuText


    def Entschlüsseln(self, Text: list[int]):
        """Takes a Text as a paramatar and returns the decryption of that text\n
        :param list Text: The text that will be decrypted
        :return str: The encrypted Text in the form of a string"""
        neutext: str = ""
        try:
            for Zahl in tqdm(Text, leave=False):
                neutext += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

        except KeyboardInterrupt:
            print(f"{Fore.RED}Entschlüsselung abgebrochen{Style.RESET_ALL}")
            print(f"{Fore.RED}Momentaner Vortschritt zurückgegeben{Style.RESET_ALL}")
            return neutext

        except Exception:
            return f"{Fore.RED}Liste oder Schlüssel ungültig{Style.RESET_ALL}"

        return neutext


    def verschlüsseln_Text(self) -> list[int]:
        """Method for encrypting a inputted Text with the Public Key of the RSA method\n
        :return list: The encrypted Text in the form of a list
        :return float: Time nessasary for the encryption"""
        Text, forcefile = self.get_Text()
        startzeit = time.time()
        if not Text and not forcefile:
            return None, 0.0

        neutext = self.Verschlüsseln(Text)
        zeit = time.time() - startzeit

        return self.check_file_creation(neutext, zeit, forcefile, "Ver")


    def Verschlüsseln_Datei(self) -> list[int]:
        """Method for encrypting a text from a choosen file\n
        :return list: The encrypted Text as a list
        :return float: Time nessasary for the encryption"""
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startzeit = time.time()
        forcefile = False
        try:
            with open(file, "r") as FileToEncrypt:
                Text = FileToEncrypt.read()
                FileToEncrypt.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.Verschlüsseln_Datei()

        if not Text:
            print(f"{Fore.RED}Die Datei hat keinen verschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.Verschlüsseln_Datei()

        elif Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        neutext = self.Verschlüsseln(Text)
        zeit = time.time() - startzeit

        return self.check_file_creation(neutext, zeit, forcefile, "Ver")


    def Entschlüsseln_Text(self) -> str:
        """Method for decrypting a text\n
        :return str: The decrypted Text as a string
        :return float: Time nessasary for the decryption"""
        Text, forcefile = self.get_Text_Ent()
        startzeit = time.time()

        if not Text and not forcefile:
            return None, 0.0

        neutext = self.Entschlüsseln(Text)
        zeit = time.time() - startzeit

        return self.check_file_creation(neutext, zeit, forcefile, "Ent")


    def Entschlüsseln_Datei(self) -> str:
        """Method for decrypting a text from a File\n
        :return str: The decrypted Text as a string
        :return float: Time nessasary for the decryption"""
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startzeit = time.time()
        forcefile: bool = False
        try:
            with open(file, "r") as FileToDecrypt:
                Text = FileToDecrypt.read()
                FileToDecrypt.close()

        except FileNotFoundError or UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        if not Text:
            print(f"{Fore.RED}Die Datei hat keinen entschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        if Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        Text = Text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
        for Zahl in Text:
            if Zahl.isdigit() and int(Zahl) < int(self.n):
                continue

            print(f"{Fore.RED}Ungültige Liste in der Datei! Richtig wäre z.B.: [400, 200]{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        NeuText: str = self.Entschlüsseln(Text)
        zeit = time.time() - startzeit

        return self.check_file_creation(NeuText, zeit, forcefile, "Ent")


    def Output_in_Datei_speichern(self, Text: str, Art: str = "RSA") -> None:
        """Method for saving an de or encrypted Text in a .txt file\n
        :param str Text: The Text that will be written into the file (str)
        :param str Art: (Optional)defines if the file contains en or decrypted Text default is "RSA"
        :return None:"""
        dateiName = f"{Art}schlüsselter Output.txt"
        currentDir = os.path.dirname(sys.argv[0])
        file = os.path.join(currentDir, dateiName)
        i = 1
        while os.path.isfile(file):
            file = os.path.join(currentDir, f"{Art}schlüsselter Output{i}.txt")
            i += 1
        with open(file, "w") as Output_File:
            Output_File.write(Text)
            Output_File.close()


    def check_file_creation(self, neuText, zeit, forceFile: bool, art: str = "RSA") -> str:
        if not len(str(neuText)) >= self.FileThreshhold and not forceFile:
            return neuText, zeit

        if len(str(neuText)) >= self.FileThreshhold ** 2 or input("Text in einer Datei speichern?(y/n): ") == "y":
            self.Output_in_Datei_speichern(str(neuText), art)
            return f"{Fore.GREEN}Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!{Style.RESET_ALL}", zeit

        return neuText, zeit


if __name__ == "__main__":
    try:
        from main import argv_check
        Debug = argv_check()
    except ImportError: Debug = False

    Programm = RSA_Verfahren(debug=Debug)
    running = True
    while running:
        running = Programm.Get_mode()