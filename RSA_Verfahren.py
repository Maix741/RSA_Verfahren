from RSA_Key_generate import Generate_Keys
from RSA_Key_split import Split_Keys
from colorama import Fore, Style
from tkinter import filedialog
import os, sys
import time


class RSA_Verfahren:
    """Class for encrypting and decrypting with RSA \n
    Initializing the object\n
    :param bool dialog: imediadly open filedialog for choosing Key file standart is False
    :param int FileThreshhold: lenght threshhold for writing en- or decryted Text in a File (int)
    :param str forcefilecreation_keyword: Keyword that if it is at the beginning of the inputs a file will always be created
    :param bool debug: Enable debug mode for viewing nessesary time for en- and decrypting
    :return None:
    """
    def __init__(self,
                 dialog: bool = False, FileThreshhold: int = 200, forcefilecreation_keyword: str = "/DateiEr", debug: bool = False
                ) -> None:
        self.modi = [
            "Ver", "Ent", "Ent Datei", "Ver Datei",                        # RSA Richtig (Abkürzungen) (0-3)
            "Verschlüsseln", "Entschlüsseln",                              # RSA Richtig (4-5)
            "Sch Generieren", "Sch teilen", "Sch auswählen", "tauschen",   # RSA Zusatz  (6-9)
            "Modi"                                                         # RSA Quality of Life (10)
            ]
        self.Optionen = f"""Verfügbare Optionen:
        1. Verschlüsseln -> "{self.modi[0]}", "{self.modi[4]}", "{self.modi[3]}"
        2. Entschlüsseln -> "{self.modi[1]}", "{self.modi[5]}", "{self.modi[2]}"
        3. Neue Schlüsselpaare generieren -> "{self.modi[6]}"
        4. Schlüssel aufteilen -> "{self.modi[7]}"
        5. Schlüsseldatei neu auswählen -> "{self.modi[8]}"
        6. Schlüssel tauschen -> "{self.modi[9]}"
        7. Diese Liste anzeigen -> "{self.modi[10]}"
        Speicherung in eine Datei zwingen -> "{forcefilecreation_keyword}" am Anfang des Textes oder der Liste
        """
        print(self.Optionen)

        self.debug: bool = debug
        self.FileThreshhold: int = FileThreshhold
        self.forcefilecreation_keyword: str = forcefilecreation_keyword

        self.D, self.E, self.n = self.load_key(dialog) # load the Key
        self.fix_modi() # FIXME: Fix this shit


    def fix_modi(self) -> None:
        """Temporary fix for Problem: Modus not in self.modi -> line 66"""
        self.modi = [mode.lower() for mode in self.modi]


    def Get_mode(self) -> bool:
        """Method for choosing RSA mode from user input \n
        :return bool: returns False when the user wnts to quit else: True
        """
        Modus = input('Modus(oder "quit"): ').lower().strip()

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus == "read_keys" and self.debug:
            print({"D": self.D, "E": self.E, "n": self.n})

        elif Modus not in self.modi:
            print(f"{Fore.RED}Ungültiger Modus!{Style.RESET_ALL}")
            return True


        # verschlüsseln, ver, ver_datei
        if Modus == self.modi[0].lower() or Modus == self.modi[4].lower():
            VerText, zeit = self.verschlüsseln_Text()
            if VerText:
                print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.RED}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")

        elif Modus == self.modi[3].lower():
            VerText, zeit = self.Verschlüsseln_Datei()
            if VerText:
                print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.RED}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")


        # entschlüsseln, ent, ent_datei
        if Modus == self.modi[1].lower() or Modus == self.modi[5].lower():
            EntText, zeit = self.Entschlüsseln_Text()
            if EntText:
                print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.RED}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")

        elif Modus == self.modi[2].lower():
            EntText, zeit = self.Entschlüsseln_Datei()
            if EntText:
                print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"{Fore.RED}Zeit zum Verschlüsseln: {zeit}{Style.RESET_ALL}")


        # generate_keys
        if Modus == self.modi[6].lower():
            Generator = Generate_Keys()
            p, q, self.n, self.E, self.D = Generator.generate_keys()
            if input("Datei erstellen(y/n): ") == "y":
                Generator.write_Keys((p, q, self.n, self.E, self.D))
                Split_Keys().create_Public_Private((self.D, self.E, self.n))

        # split_keys
        elif Modus == self.modi[7].lower():
            Split_Keys().create_Public_Private((self.D, self.E, self.n))
            print(f"{Fore.GREEN}Schlüssel erfolgreich aufgeteilt{Style.RESET_ALL}")

        # choose_key
        elif Modus == self.modi[8].lower():
            self.D, self.E, self.n = self.load_key(True)
            print(f"{Fore.RED}Schlüssel wurde erfolgreich geladen!{Style.RESET_ALL}")

        # swap Keys
        elif Modus == self.modi[9].lower():
            self.D, self.E = self.E, self.D
            print(f"{Fore.GREEN}Schlüssel wurden getauscht{Style.RESET_ALL}")

        # print Options
        elif Modus == self.modi[10]:
            print(self.Optionen)


        return True


    def Ver_oder_Entschlüsseln(self, Text: int, Schlüssel: int, n: int) -> int:
        """Method for encrypting and decrypting with RSA\n
        :param int Text: ASCII of a character (int)
        :param int Schlüssel: RSA Key (ether D or E) (int)\n
        :param int n: RSA Key fragment n (int)\n
        :return int: encrypted or decrypted Text
        """
        return pow(Text, Schlüssel, n)


    def load_key(self, dialog: bool = False) -> tuple[int]:
        """Method for loading all nessacary Key Fragments\n
        :param bool dialog: if True the path to the Key file will be choosen with a filedialog
        :return tuple: Key fragments D, E, n
        """
        currentdirectory = os.path.dirname(sys.argv[0])
        file: str = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, n, e, d = Generator.generate_keys()
                    if input("Dtei erstellen?(y/n): ").lower().strip() == "n":
                        return (d, e, n)
                    Generator.write_Keys(p, q, n, e, d)
                file = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")

        Keys: list[int] = []
        try:
            with open(file, "r") as Key_file:
                Keys = Key_file.read().splitlines()[:5]
                Key_file.close()

        except FileNotFoundError and UnicodeDecodeError:
            print(f"{Fore.RED}Es gab einen Fehler beim Lesen der Datei: {file}{Style.RESET_ALL}")
            return self.load_key(True)


        # Test Key
        if not self.test_key((Keys[2:5])):
            print(f"{Fore.RED}Ungültiger Schlüssel oder Ungültige Schlüsseldatei!{Style.RESET_ALL}")
            return self.load_key(True)

        # return D, E, n
        return (Keys.pop(4), Keys.pop(3), Keys.pop(2))


    def test_key(self, key: tuple[int]) -> bool:
        """Method for testing a RSA Key\n
        Tests if the key is a number and\n
        if de and encrypting works\n
        :param key tuple: The Key as a tuple
        :return validKey bool: returns True if the Key is valid"""
        for k in key:
            if k and k.isdigit():
                continue

            return False

        # d, e, n = key
        n, e, d = key
        testText = chr(255)
        # EntText = self.Ver_oder_Entschlüsseln(self.Ver_oder_Entschlüsseln(ord(testText), int(e), int(n)), int(d), int(n))
        VerText = self.Ver_oder_Entschlüsseln(ord(testText), int(e), int(n))
        EntText = self.Ver_oder_Entschlüsseln(VerText, int(d), int(n))
        if EntText != ord(testText):
            return False

        if self.debug:
            print(f"{Fore.GREEN}Schlüsseldatei gültig{Style.RESET_ALL}")

        return True


    def get_Text(self) -> str:
        """Method for returning encryptable Text that is compatable with the encryption method\n
        :return str: Text that would not create an Error
        """
        Text = input('Zu verschlüsselnder Text(oder "quit"): ')
        forcefile = False
        if Text:
            if Text == "quit":
                return "quit", False

            try:
                for Buchstabe in Text:
                    if ord(Buchstabe) < int(self.n):
                        continue

                    print(f"{Fore.RED}Ascii der Buchstaben darf nicht größer als {self.n} sein!{Style.RESET_ALL}")
                    return self.get_Text()

            except ValueError:
                print(f"{Fore.RED}Inkompatiebles Zeichen erkannt{Style.RESET_ALL}")
                return self.get_Text()

            if Text.startswith(self.forcefilecreation_keyword):
                Text = Text.lstrip(self.forcefilecreation_keyword)
                forcefile = True

            return Text, forcefile
        return self.get_Text()


    def get_Text_Ent(self) -> list[int]:
        """Method for returning decryptable Text that is compatable with the decryption method\n
        :return list: The list of numbers that would be decrypted
        """
        Text = input('Text(Liste) oder "quit": ').replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        forcefile = False
        if Text:
            if Text == "quit":
                return "quit", False

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

        print(f'{Fore.RED}Bitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu gehen{Style.RESET_ALL}')
        return self.get_Text_Ent()


    def verschlüsseln_Text(self) -> list[int]:
        """Method for encrypting a inputted Text with the Public Key of the RSA method\n
        :return list: The encrypted Text in the form of a list
        :return float: Time nessasary for the encryption
        """
        Text, forcefile = self.get_Text()
        startzeit = time.time()
        if Text.lower() == "quit":
            return None, 0.0

        neutext = self.Verschlüsseln(Text)

        zeit = time.time() - startzeit
        if len(neutext) >= self.FileThreshhold or forcefile:
            if input("Verschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(neutext), "Ver")
                return "Die Verschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", zeit

        return neutext, zeit


    def Verschlüsseln(self, Text: str):
        """Takes a Text as a paramatar and returns the encryption of that text\n
        :param str Text: The text that will be encrypted
        :return list: The encrypted Text in the form of a list
        """
        NeuText: list = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        return NeuText


    def Verschlüsseln_Datei(self) -> list[int]:
        """Method for encrypting a text from a choosen file\n
        :return list: The encrypted Text as a list
        :return float: Time nessasary for the encryption
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startzeit = time.time()
        forcefile = False
        try:
            with open(file, "r") as FileToEncrypt:
                Text = FileToEncrypt.read()
                FileToEncrypt.close()

        except FileNotFoundError:
            print(f"{Fore.RED}{file} konnte nicht gefunden werden!{Style.RESET_ALL}")
            return self.Verschlüsseln_Datei()

        except UnicodeDecodeError:
            print(f"{Fore.RED}Nicht Ascii Character konnte nicht Verschlüsselt werden!{Style.RESET_ALL}")
            return self.Verschlüsseln_Datei()

        if not Text:
            print(f"{Fore.RED}Die Datei hat keinen verschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.Verschlüsseln_Datei()
        
        elif Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        neutext = self.Verschlüsseln(Text)

        zeit = time.time() - startzeit
        if len(neutext) >= self.FileThreshhold or forcefile:
            if input("Verschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(neutext), "Ver")
                return "Die Verschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", zeit

        return neutext, zeit


    def Entschlüsseln_Text(self) -> str:
        """Method for decrypting a text\n
        :return str: The decrypted Text as a string
        :return float: Time nessasary for the decryption
        """
        Text, forcefile = self.get_Text_Ent()
        startzeit = time.time()

        if Text == "quit":
            return None, 0.0

        neutext = self.Entschlüsseln(Text)

        zeit = time.time() - startzeit
        if len(neutext) >= self.FileThreshhold or forcefile:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(neutext), "Ent")
                return "Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", zeit

        return neutext, zeit


    def Entschlüsseln(self, Text: str):
        """Takes a Text as a paramatar and returns the decryption of that text\n
        :param str Text: The text that will be decrypted
        :return str: The encrypted Text in the form of a string
        """
        neutext: str = ""
        try:
            for Zahl in Text:
                neutext += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

        except Exception:
            return f"{Fore.RED}Liste oder Schlüssel ungültig{Style.RESET_ALL}"
        return neutext


    def Entschlüsseln_Datei(self) -> str:
        """Method for decrypting a text from a File\n
        :return str: The decrypted Text as a string
        :return float: Time nessasary for the decryption
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return None, 0.0
        startzeit = time.time()
        forcefile = False
        try:
            with open(file, "r") as FileToDecrypt:
                Text = FileToDecrypt.read()
                FileToDecrypt.close()

        except FileNotFoundError:
            print(f"{Fore.RED}{file} konnte nicht gefunden werden!{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        except UnicodeDecodeError:
            print(f"{Fore.RED}Nicht Ascii Character konnte nicht Entschlüsselt werden!{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        if not Text:
            print(f"{Fore.RED}Die Datei hat keinen entschlüsselbaren Inhalt!{Style.RESET_ALL}")
            return self.Entschlüsseln_Datei()

        elif Text:
            if Text.startswith(self.forcefilecreation_keyword):
                Text = Text.lstrip(self.forcefilecreation_keyword)
                forcefile = True
            Text = Text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue

                print(f"{Fore.RED}Ungültige Liste eingegeben! Richtig wäre z.B.: [400, 200]{Style.RESET_ALL}")
                return self.Entschlüsseln_Datei()

        NeuText: str = self.Entschlüsseln(Text)

        zeit = time.time() - startzeit
        if len(NeuText) >= self.FileThreshhold or forcefile:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(NeuText), "Ent")
                return "Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", zeit

        return NeuText, zeit


    def Output_in_Datei_speichern(self, Text: str, Art: str = "RSA") -> None:
        """Method for saving an de or encrypted Text in a .txt file\n
        :param str Text: The Text that will be written into the file (str)
        :param str Art: (Optional)defines if the file contains en or decrypted Text default is "RSA"
        :return None:
        """
        DateiName = f"{Art}schlüsselter Output.txt"
        currentDir = os.path.dirname(sys.argv[0])
        with open(os.path.join(currentDir, DateiName), "a") as Output_File:
            Output_File.write(Text)
            Output_File.close()


if __name__ == "__main__":
    Debug = False
    if sys.argv[1:] and sys.argv[1].lower() == "debug":
        Debug = True
    Programm = RSA_Verfahren(debug=Debug)
    running = True
    while running:
        running = Programm.Get_mode()