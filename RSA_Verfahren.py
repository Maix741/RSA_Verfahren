from RSA_KEY_generate import generate_Keys, write_Keys
from tkinter import filedialog


class RSA_Verfahren:
    def __init__(self, dialog: bool = False) -> None:
        self.Optionen = """Verfügbare Optionen:
        1. Verschlüsseln -> "ver", "verschlüsseln"
        2. Entschlüsseln -> "ent", "entschlüsseln"
        3. Schlüssel aufteilen -> "split_keys"
        4. Neue Schlüssel generieren -> "generate_keys"
        5. Schlüssel neu auswählen -> "choose_key"
        """
        print(self.Optionen)
        self.D, self.E, self.n = self.load_key(dialog)


    def Get_mode(self) -> bool:
        modi = [
            "ver", "ent",                                                 # RSA Richtig (Abkürzungen) (0-1)
            "verschlüsseln", "entschlüsseln",                             # RSA Richtig (2-3)
            "generate_keys", "read_keys", "split_keys", "choose_key", "read"      # RSA Zusatz  (4-7)
            ]

        Modus = input("Modus: ").lower().replace(" ", "")

        if Modus == "q" or Modus == "quit":
            return False

        elif Modus not in modi:
            return True


        if Modus == modi[0] or Modus == modi[2]:
            VerText = self.verschlüsseln_Text()
            print(VerText)# TODO: Mehr mit Text machen
            return True


        if Modus == modi[1] or Modus == modi[3]:
            EntText = self.Entschlüsseln_Text()
            print(EntText)# TODO: Mehr mit Text machen
            return True

        if Modus == modi[4]:
            _, _, self.n, self.E, self.D = generate_Keys()
            write_Keys(_, _, self.n, self.E, self.D)

        if Modus == modi[7]:
            self.__init__(True)

        if Modus == modi[8]:
            print(self.D, self.E, self.n)

        return True
    

    def Ver_oder_Entschlüsseln(self, Text: int, S: int, n: int) -> int:
        return Text ** S % n


    def load_key(self, dialog: bool = False) -> int:
        file = "KEYS/Key.txt"
        if dialog:
            file = filedialog.askopenfilename()
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
                print("Error")
                return [0]
            return Text
        print("Error")
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
        for Zahl in Text:
            NeuText += chr(self.Ver_oder_Entschlüsseln(int(Zahl), int(self.D), int(self.n)))
        return NeuText


if __name__ == "__main__":
    Programm = RSA_Verfahren(True)
    running = True
    while running:
        running = Programm.Get_mode()