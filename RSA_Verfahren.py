from RSA_Key_generate import Generate_Keys
from RSA_Key_split import Split_Keys
from tkinter import filedialog
import os, sys
import time


class RSA_Verfahren:
    """Class for encrypting and decrypting with RSA \n
    Initialize the object\n
    :param dialog: imediadly open filedialog for choosing Key file (bool)\n
    :param speichern: immediadly create a dictionary with encryptions (bool)\n
    :param FileThreshhold: lenght threshhold for writing en- or decryted Text in a File (int)\n
    :return None:
    """
    def __init__(self, dialog: bool = False, speichern: bool = True, FileThreshhold: int = 200) -> None:
        self.modi = [
            "ver", "ent", "ent_datei", "ver_datei",                         # RSA Richtig (Abkürzungen) (0-3)
            "verschlüsseln", "entschlüsseln",                               # RSA Richtig (4-5)
            "sch_generieren", "sch_teilen", "sch_auswählen", "speichern"    # RSA Zusatz  (6-9)
            ]
        Optionen = f"""Verfügbare Optionen:
        1. Verschlüsseln -> "{self.modi[0]}", "{self.modi[4]}", "{self.modi[3]}"
        2. Entschlüsseln -> "{self.modi[1]}", "{self.modi[5]}", "{self.modi[2]}"
        3. Schlüssel aufteilen -> "{self.modi[7]}"
        4. Neue Schlüssel generieren -> "{self.modi[6]}"
        5. Schlüsseldatei neu auswählen -> "{self.modi[8]}"
        6. Verschlüsselungen speichern(erhöht geschwindigkeit drastisch) -> "{self.modi[9]}"
        """
        print(Optionen)
        self.FileThreshhold = FileThreshhold
        self.Verschlüsselung_dict = {}
        self.swapped = False
        self.D, self.E, self.n = self.load_key(dialog)
        if speichern:
            self.create_Ver_dictionary()


    def Get_mode(self) -> bool:
        Modus = input('Modus(oder "quit"): ').lower().replace(" ", "")

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus not in self.modi:
            print("Ungültiger Modus!")
            return True


        # verschlüsseln, ver, ver_datei
        if Modus == self.modi[0] or Modus == self.modi[4]:
            VerText, Zeit = self.verschlüsseln_Text()
            print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            print(f"Zeit zum Verschlüsseln: {Zeit}")

        elif Modus == self.modi[3]:
            VerText, Zeit = self.Verschlüsseln_Datei()
            print(f"\n{VerText}\n")# TODO: Mehr mit Text machen
            print(f"Zeit zum Verschlüsseln: {Zeit}")


        # entschlüsseln, ent, ent_datei
        if Modus == self.modi[1] or Modus == self.modi[5]:
            EntText, Zeit = self.Entschlüsseln_Text()
            print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            print(f"Zeit zum Entschlüsseln: {Zeit}")

        elif Modus == self.modi[2]:
            EntText, Zeit = self.Entschlüsseln_Datei()
            print(f"\n{EntText}\n")# TODO: Mehr mit Text machen
            print(f"Zeit zum Entschlüsseln: {Zeit}")


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
            print("Verschlüsselungen werden zwischengespeichert")
            self.create_Ver_dictionary()


        return True


    def Ver_oder_Entschlüsseln(self, Text: int, Schlüssel: int, n: int) -> int:
        """Method for encrypting and decrypting with RSA\n
        :param Text: ASCII of a character (int)
        :param Schlüssel: RSA Key (ether D or E) (int)\n
        :param n: RSA Key fragment n (int)\n
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

        for ascii in range(255):
            Buchstaben.append(chr(ascii))

        Verschlüsselungen = []
        for Buchstabe in Buchstaben:
            Verschlüsselungen.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        self.Verschlüsselung_dict.clear()
        for Buch, verschlüsselung in zip(Buchstaben, Verschlüsselungen):
            self.Verschlüsselung_dict[verschlüsselung] = Buch
        Verschlüsselungen.clear()
        Buchstaben.clear()


    def load_key(self, dialog: bool = False) -> int:
        """Method for loading all nessacary Key Fragments\n
        :param dialog: if True the path to the Key file will be choosen with a filedialog
        :return int: Key fragments D, E, n
        """
        file = "KEYS/RSA_Key.txt"
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, self.n, self.E, self.D = Generator.generate_keys()
                    if input("Datei erstellen(y/n): ") == "y":
                        Generator.write_Keys(p, q, self.n, self.E, self.D)
                file = "KEYS/RSA_Key.txt"

        Keys = []
        self.swapped = False
        try:
            with open(file, "r") as Key_file:
                for line in Key_file.readlines():
                    Keys.append(line.rstrip())
                Key_file.close()
        except FileNotFoundError:
            print(f"FileNotFoundError: {file} nicht gefunden!")
            return self.load_key(True)

        # return D, E, n
        return Keys.pop(4), Keys.pop(3), Keys.pop(2)


    def get_Text(self) -> str:
        """Method for returning encryptable Text that is compatable with the encryption method\n
        :return str: Text that would not create an Error
        """
        Text = input('Zu verschlüsselnder Text(oder "quit"): ')
        if Text:
            try:
                for Buchstabe in Text:
                    if ord(Buchstabe) < int(self.n):
                        continue

                    print(f"ValueError: Ascii des Buchstaben größer als {self.n}")
                    return self.get_Text()

            except ValueError:
                print("ValueError: Inkompatiebles Zeichen")
                return self.get_Text()

            return Text
        return self.get_Text()


    def get_Text_Ent(self) -> list:
        """Method for returning decryptable Text that is compatable with the decryption method\n
        :return list: The list of numbers that would be decrypted
        """
        Text = input("Text(list): ").replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        if Text:
            if Text == "quit":
                return "quit"

            Text = Text.split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue

                print(f"\nValueError: Input muss eine Liste von ints unter {self.n} sein!")
                return self.get_Text_Ent()
            return Text

        print(f"\nValueError: Kein Input erkannt!")
        return self.get_Text_Ent()


    def verschlüsseln_Text(self) -> list:
        """Method for creating a dictionary for encryptions for ASCII(0-255) with the Public Key\n
        :return list, int: The encrypted Text in the form of a list and the time nessasary for the encrytion
        """
        Text = self.get_Text()
        StartZeit = time.time()
        if Text.lower() == "quit":
            return "Verschlüsselung abgebrochen!", 0.0
        NeuText: list = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        Zeit = round(time.time() - StartZeit, 2)
        if len(NeuText) > self.FileThreshhold:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(NeuText), "Ver")
                return "Die Verschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", Zeit

        return NeuText, Zeit


    def Entschlüsseln_Text(self) -> str:
        """Method for decrypting a text\n
        :return str: The decrypted Text as a string
        """
        Text = self.get_Text_Ent()
        NeuText: str = ""
        StartZeit = time.time()

        if Text == "quit":
            return "Entschlüsselung abgebrochen", 0.0

        if self.Verschlüsselung_dict:
            for Zahl in Text:
                Buch: str = str(self.Verschlüsselung_dict.get(int(Zahl)))
                if Buch == "None" or not Buch:
                    Buch: str = chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

                NeuText += Buch

        elif not self.Verschlüsselung_dict:
            print("Verschlüsselungen nicht zwischengespeichert!")
            print("Das Entschlüsseln könnte einige Zeit dauern, bitte Warten!")
            for Zahl in Text:
                NeuText += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

        Zeit = round(time.time() - StartZeit, 2)
        if len(NeuText) > self.FileThreshhold:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(NeuText), "Ent")
                return "Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", Zeit

        return NeuText, Zeit


    def Entschlüsseln_Datei(self) -> str:
        """Method for decrypting a text from a File\n
        :return str: The decrypted Text as a string
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        StartZeit = time.time()
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            print(f"\nValueError: Keine Datei erkannt!")
            return self.Entschlüsseln_Datei()
        if Text:
            Text = Text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue
                print(f"\nValueError: Liste Ungültig!")
                return self.Entschlüsseln_Datei()

        NeuText = ""
        if not self.Verschlüsselung_dict:
            for Zahl in Text:
                NeuText += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

        elif self.Verschlüsselung_dict:
            print("Dictionary erkannt")
            for Zahl in Text:
                Buch = str(self.Verschlüsselung_dict.get(int(Zahl)))
                if Buch == "None":
                    Buch = chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

                NeuText += Buch

        Zeit = time.time() - StartZeit
        if len(NeuText) > self.FileThreshhold:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(NeuText), "Ent")
                return "Die Entschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", Zeit

        return NeuText, Zeit


    def Verschlüsseln_Datei(self) -> list:
        """Method for encrypting a text\n
        :return list, float: The encrypted Text as a list and the nessesary time
        """
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        StartZeit = time.time()
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            print(f"\nFileNotFoundError: Keine Datei erkannt!")
            return self.Verschlüsseln_Datei()

        except not Text:
            print(f"\nValueError Datei hat keinen verschlüsselbaren Inhalt!")
            return self.Verschlüsseln_Datei()

        NeuText = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(int(ord(Buchstabe)), int(self.E), int(self.n)))

        Zeit = round(time.time() - StartZeit, 2)
        if len(NeuText) > self.FileThreshhold:
            if input("Entschlüselten Text in Datei speichern?(y/n): ") == "y":
                self.Output_in_Datei_speichern(str(NeuText), "Ver")
                return "Die Verschlüsselte Nachricht wurde erfolgreich in einer Datei gespeichert!", Zeit

        return NeuText, Zeit


    def Output_in_Datei_speichern(self, Text: str, Art: str = "RSA") -> None:
        """Method for saving an de or encrypted Text in a .txt file\n
        :param Text: The Text that will be written into the file (str)
        :param Art: (Optional)defines if the file contains en or decrypted Text default is "RSA"
        :return None:
        """
        DateiName = f"{Art}schlüsselter Output.txt"
        currentDir = os.path.dirname(sys.argv[0])
        with open(os.path.join(currentDir, DateiName), "a") as Output_File:
            Output_File.write(Text)
            Output_File.close()


if __name__ == "__main__":
    Programm = RSA_Verfahren()
    running = True
    while running:
        running = Programm.Get_mode()


# Geschwindigkeit Entschlüsseln für 100 Wörter Lorem Ipsum:
    # Ohne dictionary: 219.78877234458923 Sekunden
    # Mit dictionary: 0.0009968280792236328 Sekunden

# Geschwindigkeit Entschlüsseln für 1000 Wörter Lorem Ipsum:
    # Ohne dictionary: 2236.4441187381744 Sekunden
    # Mit dictionary: 0.008044004440307617 Sekunden