from RSA_KEY_generate import generate_Keys, write_Keys, create_Public_Private
from tkinter import filedialog
import os, sys
import time


class RSA_Verfahren:
    def __init__(self, dialog: bool = False) -> None:
        self.Optionen = """Verfügbare Optionen:
        1. Verschlüsseln -> "ver", "verschlüsseln"
        2. Entschlüsseln -> "ent", "entschlüsseln"
        3. Schlüssel aufteilen -> "split_keys"
        4. Neue Schlüssel generieren -> "generate_keys"
        5. Schlüsseldatei neu auswählen -> "choose_key"
        6. Verschlüsselungen speichern(erhöht geschwindigkeit) -> "speichern"
        """
        print(self.Optionen)
        self.Verschlüsselung_dict = {}
        self.D, self.E, self.n = self.load_key(dialog)


    def Get_mode(self) -> bool:
        modi = [
            "ver", "ent",                                                              # RSA Richtig (Abkürzungen) (0-1)
            "verschlüsseln", "entschlüsseln",                                          # RSA Richtig (2-3)
            "generate_keys", "split_keys", "choose_key", "speichern", "read_keys"      # RSA Zusatz  (4-8)
            ]

        Modus = input(f"Modus(oder {"quit"}): ").lower().replace(" ", "")

        # check if Mode is valid or quit
        if Modus == "q" or Modus == "quit":
            return False

        elif Modus not in modi:
            return True


        # verschlüsseln, ver
        if Modus == modi[0] or Modus == modi[2]:
            VerText = self.verschlüsseln_Text()
            print(VerText)# TODO: Mehr mit Text machen


        # entschlüsseln, ent
        if Modus == modi[1] or Modus == modi[3]:
            EntText = self.Entschlüsseln_Text()
            print(EntText)# TODO: Mehr mit Text machen
            Zeit = time.time() - self.Start


        # generate_keys
        if Modus == modi[4]:
            _, _, self.n, self.E, self.D = generate_Keys()
            write_Keys(_, _, self.n, self.E, self.D)

        if Modus == modi[6]:
            create_Public_Private()

        # choose_key
        if Modus == modi[6]:
            self.__init__(True)
            self.Verschlüsselung_dict = {}
            if input("Speichern?(y/n): ").lower() == "y":
                self.create_Ver_dictionary()

        # read_keys
        if Modus == modi[8]:
            print(self.D, self.E, self.n, "D, E, n")

        # speichern
        if Modus == modi[7]:
            print("Verschlüsselungen werden zwischengespeichert")
            self.create_Ver_dictionary()

        return True
    

    def Ver_oder_Entschlüsseln(self, Text: int, S: int, n: int) -> int:
        return Text ** S % n


    def create_Ver_dictionary(self) -> dict:
        Buchstaben = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ü", "ä", "ö",
                      "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ü", "Ä", "Ö",
                       " ", ",", ".", "!", "?"]
        Verschlüsselungen = []
        for Buchstabe in Buchstaben:
            Verschlüsselungen.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))

        for Buch, verschlüsselung in zip(Buchstaben, Verschlüsselungen):
            self.Verschlüsselung_dict[verschlüsselung] = Buch
        Verschlüsselungen.clear()


    def load_key(self, dialog: bool = False) -> int:
        file = "KEYS/Key.txt"
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                file = "KEYS/Key.txt"

        Keys = []
        with open(file, "r") as Key_file:
            for line in Key_file.readlines():
                Keys.append(line.rstrip())
            Key_file.close()

        # return D, E, n
        return Keys.pop(4), Keys.pop(3), Keys.pop(2)


    def get_Text(self) -> str:
        Text = input("Text: ")
        if Text:
            try:
                for Buchstabe in Text:
                    if ord(Buchstabe) < int(self.n):
                        continue
                    return "Error"
            except ValueError:
                return "Error"
            return Text


    def get_Text_Ent(self):
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
        print(f"\nValueError: Input muss eine Liste von ints unter {self.n} sein!")
        return [0]


    def verschlüsseln_Text(self) -> list:
        Text = self.get_Text()
        if Text == "Error":
            return Text
        NeuText = []
        for Buchstabe in Text:
            NeuText.append(self.Ver_oder_Entschlüsseln(ord(Buchstabe), int(self.E), int(self.n)))
        return NeuText


    def Entschlüsseln_Text(self):
        Text = self.get_Text_Ent()
        NeuText = ""
        self.Start = time.time()
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


if __name__ == "__main__":
    Programm = RSA_Verfahren()
    running = True
    while running:
        running = Programm.Get_mode()

# Geschwindigkeit für 100 Wörter Lorem Ipsum
    # Ohne dictionary: 219.78877234458923 Sekunden
    # Mit dictionary: 0.0009968280792236328