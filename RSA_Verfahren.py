from RSA_KEY_generate import generate_Keys, write_Keys, create_Public_Private
from tkinter import filedialog
import os, sys
import time


class RSA_Verfahren:
    """Klasse mit Funktionen zum Ver-\n
      und Entschlüsseln mit dem RSA Verfahren"""
    def __init__(self, dialog: bool = False, speichern: bool = True) -> None:
        self.Optionen = """Verfügbare Optionen:
        1. Verschlüsseln -> "ver", "verschlüsseln", "ver_Datei
        2. Entschlüsseln -> "ent", "entschlüsseln", "ent_Datei"
        3. Schlüssel aufteilen -> "split_keys"
        4. Neue Schlüssel generieren -> "generate_keys"
        5. Schlüsseldatei neu auswählen -> "choose_key"
        6. Verschlüsselungen speichern(erhöht geschwindigkeit drastisch) -> "speichern"
        """
        print(self.Optionen)
        self.Verschlüsselung_dict = {}
        self.D, self.E, self.n = self.load_key(dialog)
        if speichern:
            self.create_Ver_dictionary()


    def Get_mode(self) -> bool:
        modi = [
            "ver", "ent", "ent_datei", "ver_datei",                                    # RSA Richtig (Abkürzungen) (0-3)
            "verschlüsseln", "entschlüsseln",                                          # RSA Richtig (4-5)
            "generate_keys", "split_keys", "choose_key", "speichern", "read_keys"      # RSA Zusatz  (6-10)
            ]

        Modus = input('Modus(oder "quit"): ').lower().replace(" ", "")

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus not in modi:
            print("Ungültiger Modus!")
            return True


        # verschlüsseln, ver
        if Modus == modi[0] or Modus == modi[4]:
            VerText = self.verschlüsseln_Text()
            print(VerText)# TODO: Mehr mit Text machen
            Zeit = round(time.time() - self.Start_Ver, 2)
            print(f"Zeit zum Verschlüsseln: {Zeit}")

        elif Modus == modi[3]:
            VerText = self.Verschlüsseln_Datei()
            print(VerText)# TODO: Mehr mit Text machen
            Zeit = round(time.time() - self.Start_Ver_Datei, 2)
            print(f"Zeit zum Entschlüsseln: {Zeit}")


        # entschlüsseln, ent
        if Modus == modi[1] or Modus == modi[5]:
            EntText = self.Entschlüsseln_Text()
            print(EntText)# TODO: Mehr mit Text machen
            Zeit = round(time.time() - self.Start_Ent, 2)
            print(f"Zeit zum Entschlüsseln: {Zeit}")

        elif Modus == modi[2]:
            EntText = self.Entschlüsseln_Datei()
            print(EntText)# TODO: Mehr mit Text machen
            Zeit = round(time.time() - self.Start_Ent_Datei, 2)
            print(f"Zeit zum Entschlüsseln: {Zeit}")


        # generate_keys
        if Modus == modi[6]:
            _, _, self.n, self.E, self.D = generate_Keys()
            write_Keys(_, _, self.n, self.E, self.D)

        # split_keys
        if Modus == modi[7]:
            create_Public_Private()

        # choose_key
        if Modus == modi[8]:
            self.__init__(True)
            self.Verschlüsselung_dict = {}
            if input("Speichern?(y/n): ").lower() == "y":
                self.create_Ver_dictionary()

        # speichern
        if Modus == modi[9]:
            print("Verschlüsselungen werden zwischengespeichert")
            self.create_Ver_dictionary()
            
        # read_keys
        if Modus == modi[10]:
            print(f"{self.D}, {self.E}, {self.n}\t# D, E, n")


        return True


    def Ver_oder_Entschlüsseln(self, Text: int, S: int, n: int) -> int:
        return Text ** S % n


    def create_Ver_dictionary(self) -> None:
        # Buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ü", "ä", "ö",
        #               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ü", "Ä", "Ö",
        #               " ", ",", ";", ".", ":", "!", "?", '"', "'", "#", "*", "&"]
        Buchstaben = []

        for ascii in range(255):
            Buchstaben.append(chr(ascii))

        Verschlüsselungen = []
        for Buchstabe in Buchstaben:
            Verschlüsselungen.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        for Buch, verschlüsselung in zip(Buchstaben, Verschlüsselungen):
            self.Verschlüsselung_dict[verschlüsselung] = Buch
        Verschlüsselungen.clear()


    def load_key(self, dialog) -> int:
        file = "KEYS/RSA_Key.txt"
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                file = "KEYS/RSA_Key.txt"

        Keys = []
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
        Text = input("Zu verschlüsselnder Text: ")
        if Text:
            try:
                for Buchstabe in Text:
                    if ord(Buchstabe) < int(self.n):
                        continue
                    return f"ValueError: Buchstabe größer als {self.n}"
            except ValueError:
                return "ValueError: Inkompatiebles Zeichen"
            return Text
        return "ValueError: Kein Text eingegeben"


    def get_Text_Ent(self) -> list:
        Text = input("Text(list): ").replace("[", "").replace("'", "").replace("]", "").replace(" ", "")
        if Text:
            Text = Text.split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue
                print(f"\nValueError: Input muss eine Liste von ints unter {self.n} sein!")
                return [0]
            return Text
        print(f"\nValueError: Kein Input erkannt!")
        return [0]


    def verschlüsseln_Text(self) -> list:
        Text = self.get_Text()
        self.Start_Ver = time.time()
        if Text.startswith("ValueError"):
            return Text
        NeuText = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))
        return NeuText


    def Entschlüsseln_Text(self) -> str:
        Text = self.get_Text_Ent()
        NeuText: str = ""
        self.Start_Ent = time.time()
        if not self.Verschlüsselung_dict:
            for Zahl in Text:
                NeuText += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))
            return NeuText

        elif self.Verschlüsselung_dict:
            print("Dictionary erkannt")
            for Zahl in Text:
                Buch: str = str(self.Verschlüsselung_dict.get(int(Zahl)))
                if Buch == "None":
                    Buch: str = chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

                NeuText += Buch

            return NeuText


    def Entschlüsseln_Datei(self) -> str:
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        self.Start_Ent_Datei = time.time()
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            return f"\nValueError: Keine Datei erkannt!"
        if Text:
            Text = Text.replace("[", "").replace("'", "").replace("]", "").replace(" ", "").split(",")
            for Zahl in Text:
                if Zahl.isdigit():
                    if int(Zahl) < int(self.n):
                        continue
                return f"\nValueError: Liste Ungültig!"

        NeuText = ""
        if not self.Verschlüsselung_dict:
            for Zahl in Text:
                NeuText += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))
            return NeuText

        elif self.Verschlüsselung_dict:
            print("Dictionary erkannt")
            for Zahl in Text:
                Buch = str(self.Verschlüsselung_dict.get(int(Zahl)))
                if Buch == "None":
                    Buch = chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))

                NeuText += Buch

            return NeuText


    def Verschlüsseln_Datei(self) -> str:
        file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"),("All Files", "*.*")], title="Datei auswählen")
        self.Start_Ver_Datei = time.time()
        try:
            with open(file, "r") as File:
                Text = File.read()
                File.close()
        except FileNotFoundError:
            return f"\nFileNotFoundError: Keine Datei erkannt!"

        if not Text:
            return f"\nValueError Datei hat keinen verschlüsselbaren Inhalt!"

        NeuText = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(int(ord(Buchstabe)), int(self.E), int(self.n)))

        return NeuText


if __name__ == "__main__":
    Programm = RSA_Verfahren()
    running = True
    while running:
        running = Programm.Get_mode()


# Geschwindigkeit für 100 Wörter Lorem Ipsum:
    # Ohne dictionary: 219.78877234458923 Sekunden
    # Mit dictionary: 0.0009968280792236328 Sekunden

# Geschwindigkeit für 1000 Wörter Lorem Ipsum:
    # Ohne dictionary: 2236.4441187381744 Sekunden
    # Mit dictionary: 0.008044004440307617 Sekunden