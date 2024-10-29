from RSA_Key_generate import Generate_Keys
from tkinter import filedialog
import os, sys


class Split_Keys:
    def __init__(self) -> None:
        self.currentDir = os.path.dirname(sys.argv[0])
        os.chdir(self.currentDir)
        self.create_Folder_structure(self.currentDir)


    def load_key(self, dialog: bool = False) -> tuple:
        """Method for loading all nessacary Key Fragments\n
        :param bool dialog: if True the path to the Key file will be choosen with a filedialog
        :return tuple: Key fragments D, E, n
        """
        currentdirectory = os.path.dirname(sys.argv[0])
        file = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")
        if dialog:
            file = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]), filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Key Datei auswählen")
            if not file:
                if input("Schlüssel generieren?(y/n): ") == "y":
                    Generator = Generate_Keys()
                    p, q, n, e, d = Generator.generate_keys()
                    Generator.write_Keys(p, q, n, e, d)
                file = os.path.join(currentdirectory, "KEYS", "RSA_Key.txt")

        Keys = []
        try:
            with open(file, "r") as Key_file:
                Keys = Key_file.read().splitlines()
                Key_file.close()

        except FileNotFoundError:
            print(f"{file} konnte nicht gefunden werden!")
            return self.load_key(True)

        for key in Keys:
            if Keys.index(key) >= 5:
                break
            if key and key.isdigit():
                continue

            print("Ungültige oder leere Schlüsseldatei!")
            return self.load_key(True)

        # return D, E, n
        return (Keys.pop(4), Keys.pop(3), Keys.pop(2))


    def create_Folder_structure(self, rootDir) -> None:
        try:
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt"))
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt", "PUBLIC"))
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt", "PRIVATE"))

        except FileExistsError:
            pass


    def create_Public_Private(self, key: tuple = None) -> None:
        if key:
            d, e, n = key
        else:
            d, e, n = self.load_key(True)

        self.write_Private(n, d)
        self.write_Public(n, e)


    def write_Public(self, n: int, e: int) -> None:
        Publicfile = os.path.join(self.currentDir, "RSA_Geteilt", "PUBLIC", "PUBLIC_Key.txt")
        with open(Publicfile, "w") as Public:
            Public.write(f"{n}\n{e}\n\n# n, E")
            Public.close()


    def write_Private(self, n: int, d: int) -> None:
        Privatefile = os.path.join(self.currentDir, "RSA_Geteilt", "PRIVATE", "PRIVATE_Key.txt")
        with open(Privatefile, "w") as Private:
            Private.write(f"{n}\n{d}\n\n# n, D")
            Private.close()


if __name__ == "__main__":
    Split_Keys().create_Public_Private()