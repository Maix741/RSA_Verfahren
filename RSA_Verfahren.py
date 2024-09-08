from RSA_Key_generate import Generate_Keys
from RSA_Key_split import Split_Keys
from tkinter import filedialog
import os, sys
import time


class RSA_Verfahren:
    """Class for encrypting and decrypting with RSA \n
    Initialize the object\n
    :param bool dialog: imediadly open filedialog for choosing Key file standart is False\n
    :param bool speichern: immediadly create a dictionary with encryptions (bool)\n
    :param int FileThreshhold: lenght threshhold for writing en- or decryted Text in a File (int)\n
    :param int known_charactars_ascii_range: end of range of ascii characters that will be added to the dictionarys "all" would be all posseble ascii codes\n
    :return None:
    """
    def __init__(self, dialog: bool = False, speichern: bool = True, FileThreshhold: int = 200, known_charactars_ascii_range: int = 255, forcefilecreation_keyword: str = "/DateiEr", debug: bool = False) -> None:
        self.modi = [
            "ver", "ent", "ent_datei", "ver_datei",                         # RSA Richtig (Abkürzungen) (0-3)
            "verschlüsseln", "entschlüsseln",                               # RSA Richtig (4-5)
            "sch_generieren", "sch_teilen", "sch_auswählen", "speichern"    # RSA Zusatz  (6-9)
            ]
        Optionen = f"""Verfügbare Optionen:
        1. Verschlüsseln -> "{self.modi[0]}", "{self.modi[4]}", "{self.modi[3]}"
        2. Entschlüsseln -> "{self.modi[1]}", "{self.modi[5]}", "{self.modi[2]}"
        3. Neue Schlüssel generieren -> "{self.modi[6]}"
        4. Schlüssel aufteilen -> "{self.modi[7]}"
        5. Schlüsseldatei neu auswählen -> "{self.modi[8]}"
        6. Verschlüsselungen speichern(erhöht geschwindigkeit drastisch) -> "{self.modi[9]}"
        Speicherung in eine Datei zwingen -> "{forcefilecreation_keyword}" am Anfang des Textes oder der Liste
        """
        print(Optionen)
        self.debug = debug
        if known_charactars_ascii_range == "all":
            known_charactars_ascii_range = int(0x110000)
        self.known_charactars_ascii_range = known_charactars_ascii_range
        self.FileThreshhold = FileThreshhold
        self.forcefilecreation_keyword = forcefilecreation_keyword
        self.dictionary_zum_entschlüsseln = {}
        self.dictionary_zum_verschlüsseln = {}
        # self.swapped = False
        self.D, self.E, self.n = self.load_key(dialog)
        if self.debug:
            print(self.D, self.E, self.n)
        if speichern:
            self.create_Ver_dictionary()


    def Get_mode(self) -> bool:
        """Method for choosing RSA mode from user input \n
        :return bool: returns False when the user wnts to quit else: True
        """
        Modus = input('Modus(oder "quit"): ').lower().replace(" ", "")

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus not in self.modi:
            print("Ungültiger Modus!")
            return True


        # verschlüsseln, ver, ver_datei
        if Modus == self.modi[0] or Modus == self.modi[4]:
            VerText, zeit = self.verschlüsseln_Text()
            print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"Zeit zum Verschlüsseln: {zeit}")

        elif Modus == self.modi[3]:
            VerText, zeit = self.Verschlüsseln_Datei()
            print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"Zeit zum Verschlüsseln: {zeit}")


        # entschlüsseln, ent, ent_datei
        if Modus == self.modi[1] or Modus == self.modi[5]:
            EntText, zeit = self.Entschlüsseln_Text()
            print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"Zeit zum Entschlüsseln: {zeit}")

        elif Modus == self.modi[2]:
            EntText, zeit = self.Entschlüsseln_Datei()
            print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            if self.debug:
                print(f"Zeit zum Entschlüsseln: {zeit}")


        # generate_keys
        if Modus == self.modi[6]:
            Generator = Generate_Keys()
            p, q, self.n, self.E, self.D = Generator.generate_keys()
            if input("Datei erstellen(y/n): ") == "y":
                Generator.write_Keys(p, q, self.n, self.E, self.D)
                Split_Keys().create_Public_Private()

        # split_keys
        elif Modus == self.modi[7]:
            Split_Keys().create_Public_Private()
            print("Schlüssel erfolgreich aufgeteilt")

        # choose_key
        elif Modus == self.modi[8]:
            self.D, self.E, self.n = self.load_key(True)
            if input("Speichern?(y/n): ").lower() == "y":
                self.create_Ver_dictionary()

        # speichern
        elif Modus == self.modi[9]:
            ende_range = input("Ascii Ende des Wörterbuchs: ")
            if ende_range == "all":
                self.known_charactars_ascii_range = int(0x110000)
            elif ende_range and ende_range.isdigit() and int(ende_range) <= int(0x110000):
                self.known_charactars_ascii_range = int(ende_range)
            print("Verschlüsselungen werden zwischengespeichert")
            self.create_Ver_dictionary()


        return True


    def Ver_oder_Entschlüsseln(self, Text: int, Schlüssel: int, n: int) -> int:
        """Method for encrypting and decrypting with RSA\n
        :param int Text: ASCII of a character (int)
        :param int Schlüssel: RSA Key (ether D or E) (int)\n
        :param int n: RSA Key fragment n (int)\n
        :return int: encrypted or decrypted Text
        """
        return Text ** Schlüssel % n


    def create_Ver_dictionary(self) -> None:
        """Method for creating a dictionary for encryptions for ASCII(0-255) with the Public Key\n
        :return None:
        """
        # Buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ü", "ä", "ö",
        #               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ü", "Ä", "Ö",
        #               " ", ",", ";", ".", ":", "!", "?", '"', "'", "#", "*", "&"]
        Buchstaben = []

        Start = time.time()
        for ascii in range(self.known_charactars_ascii_range):
            Buchstaben.append(chr(ascii))

        Verschlüsselungen = []
        for Buchstabe in Buchstaben:
            Verschlüsselungen.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        self.dictionary_zum_entschlüsseln.clear()
        self.dictionary_zum_verschlüsseln.clear()
        for buchstabe, verschlüsselung in zip(Buchstaben, Verschlüsselungen):
            self.dictionary_zum_entschlüsseln[verschlüsselung] = buchstabe
            self.dictionary_zum_verschlüsseln[buchstabe] = verschlüsselung
        Verschlüsselungen.clear()
        Buchstaben.clear()
        if self.debug:
            print(f"Benötigte Zeit zum Speichern: {round(time.time() - Start, 5)} Sekunden")


    def load_key(self, dialog: bool = False) -> int:
        """Method for loading all nessacary Key Fragments\n
        :param bool dialog: if True the path to the Key file will be choosen with a filedialog
        :return int: Key fragments D, E, n
        """
        currentdirectory = os.path.dirname(sys.argv[0])
        file = os.path.join(currentdirectory, r"KEYS\RSA_Key.txt")
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, self.n, self.E, self.D = Generator.generate_keys()
                    if input("Datei erstellen(y/n): ") == "y":
                        Generator.write_Keys(p, q, self.n, self.E, self.D)
                file = os.path.join(currentdirectory, r"KEYS\RSA_Key.txt")

        Keys = []
        # self.swapped = False
        try:
            with open(file, "r") as Key_file:
                for line in Key_file.readlines():
                    Keys.append(line.rstrip())
                Key_file.close()
        except FileNotFoundError:
            print(f"{file} konnte nicht gefunden werden!")
            return self.load_key(True)

        if not Keys:
            print("Leere Schlüsseldatei!")
            return self.load_key(True)

        for key in Keys:
            if Keys.index(key) >= 5:
                break
            if key and key.isdigit():
                continue

            print("Ungültige Schlüsseldatei!")
            return self.load_key(True)

        # return D, E, n
        return Keys.pop(4), Keys.pop(3), Keys.pop(2)


    def get_Text(self) -> str:
        """Method for returning encryptable Text that is compatable with the encryption method\n
        :return str: Text that would not create an Error
        """
        Text = input('Zu verschlüsselnder Text(oder "quit"): ')
        forcefile = False
        if Text:
            if Text == "quit":
                return "quit"

            try:
                for Buchstabe in Text:
                    if ord(Buchstabe) < int(self.n):
                        continue

                    print(f"Ascii der Buchstaben darf nicht größer als {self.n} sein!")
                    return self.get_Text()

            except ValueError:
                print("Inkompatiebles Zeichen erkannt")
                return self.get_Text()

            if Text.startswith(self.forcefilecreation_keyword):
                Text = Text.lstrip(self.forcefilecreation_keyword)
                forcefile = True

            return Text, forcefile
        return self.get_Text()


    def get_Text_Ent(self) -> list:
        """Method for returning decryptable Text that is compatable with the decryption method\n
        :return list: The list of numbers that would be decrypted
        """
        Text = input("Text(list): ").replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        forcefile = False
        if Text:
            if Text == "quit":
                return "quit"

            if Text.startswith(self.forcefilecreation_keyword):
                Text = Text.lstrip(self.forcefilecreation_keyword)
                forcefile = True

            Text = Text.split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue

                print(f"\nEingabe muss eine Liste von ganzen Zahlen unter {self.n} sein!")
                return self.get_Text_Ent()
            return Text, forcefile

        print(f'\nBitte geben sie einen Text ein! Oder schreiben sie "quit" um zurück zu gehen')
        return self.get_Text_Ent()


    def verschlüsseln_Text(self) -> list:
        """Method for encrypting a inputted Text with the Public Key of the RSA method\n
        :return list: The encrypted Text in the form of a list
        :return float: Time nessasary for the encryption
        """
        Text, forcefile = self.get_Text()
        startzeit = time.time()
        if Text.lower() == "quit":
            return "Verschlüsselung abgebrochen!", 0.0

        neutext = self.Verschlüsseln(Text)

        zeit = round(time.time() - startzeit, 2)
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
        if self.dictionary_zum_verschlüsseln:
            for buchstabe in Text:
                verschlüsselung: int = self.dictionary_zum_verschlüsseln.get(buchstabe)
                if verschlüsselung == "None" or not verschlüsselung:
                    verschlüsselung: int = self.Ver_oder_Entschlüsseln(ord(buchstabe), int(self.E), int(self.n))

                NeuText.append(verschlüsselung)
        elif not self.dictionary_zum_verschlüsseln:
            print("Keine Zwischenspeicherung gefunden! Bitte warten")
            print("Das Verschlüsseln könnte einige Zeit dauern, bitte Warten!")
            for Buchstabe in Text:
                NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        return NeuText


    def Verschlüsseln_Datei(self) -> list:
        """Method for encrypting a text from a choosen file\n
        :return list: The encrypted Text as a list 
        :return float: Time nessasary for the encryption
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return "Die Verschlüsselung wurde abgebrochen!", 0.0
        startzeit = time.time()
        forcefile = False
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            print(f"\n{file} konnte nicht gefunden werden!")
            return self.Verschlüsseln_Datei()
        
        except UnicodeDecodeError:
            print("Nicht Ascii Character konnte nicht Verschlüsselt werden!")
            return self.Verschlüsseln_Datei()

        if not Text:
            print(f"\nDie Datei hat keinen verschlüsselbaren Inhalt!")
            return self.Verschlüsseln_Datei()
        
        elif Text.startswith(self.forcefilecreation_keyword):
            Text = Text.lstrip(self.forcefilecreation_keyword)
            forcefile = True

        neutext = self.Verschlüsseln(Text)

        zeit = round(time.time() - startzeit, 2)
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
            return "Entschlüsselung abgebrochen", 0.0

        neutext = self.Entschlüsseln(Text)

        zeit = round(time.time() - startzeit, 2)
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
        if self.dictionary_zum_entschlüsseln:
            for Zahl in Text:
                Buch: str = str(self.dictionary_zum_entschlüsseln.get(int(Zahl)))
                if Buch == "None" or not Buch:
                    try:
                        Buch: str = chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))
                    except ValueError:
                        print(f'Error "{Zahl}" konnte mit dem Schlüssel nicht Entschlüsselt werden!')
                        continue

                neutext += Buch

        elif not self.dictionary_zum_entschlüsseln:
            print("Verschlüsselungen nicht zwischengespeichert!")
            print("Das Entschlüsseln könnte einige Zeit dauern, bitte Warten!")
            for Zahl in Text:
                neutext += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

        return neutext


    def Entschlüsseln_Datei(self) -> str:
        """Method for decrypting a text from a File\n
        :return str: The decrypted Text as a string
        :return float: Time nessasary for the decryption
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        if not file:
            return "Die Entschlüsselung wurde abgebrochen!", 0.0
        startzeit = time.time()
        forcefile = False
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            print(f"\n{file} konnte nicht gefunden werden!")
            return self.Entschlüsseln_Datei()
        if Text:
            if Text.startswith(self.forcefilecreation_keyword):
                Text = Text.lstrip(self.forcefilecreation_keyword)
                forcefile = True
            Text = Text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue

                print(f"\nUngültige Liste eingegeben! Richtig wäre z.B.: 400, 200")
                return self.Entschlüsseln_Datei()

        NeuText: str = self.Entschlüsseln(Text)

        zeit = round(time.time() - startzeit, 2)
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
    DEBUG = False
    if sys.argv[1:]:
        if sys.argv[1].lower() == "debug":
            DEBUG = True
    Programm = RSA_Verfahren(debug=DEBUG)
    running = True
    while running:
        running = Programm.Get_mode()


# Geschwindigkeit Entschlüsseln für 100 Wörter Lorem Ipsum:
    # Ohne dictionary: 219.78877234458923 Sekunden
    # Mit dictionary: 0.0009968280792236328 Sekunden

# Geschwindigkeit Entschlüsseln für 1000 Wörter Lorem Ipsum:
    # Ohne dictionary: 2236.4441187381744 Sekunden
    # Mit dictionary: 0.008044004440307617 Sekunden

# Geschwindigkeit Wörterbuch erstellen:
    # alle Möglichen Zeichen: 1.3275301456451416 Sekunden