from RSA_Key_generate import Generate_Keys
from colorama import Fore, Style
from tkinter import filedialog
import os, sys


class Split_Keys:
    def __init__(self) -> None:
        self.currentDir = os.path.dirname(sys.argv[0])
        os.chdir(self.currentDir)
        self.create_Folder_structure(self.currentDir)


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

        # return D, E, n
        return (Keys.pop(4), Keys.pop(3), Keys.pop(2))


    def create_Folder_structure(self, rootDir: str) -> None:
        try:
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt"))
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt", "PUBLIC"))
            os.mkdir(os.path.join(rootDir, "RSA_Geteilt", "PRIVATE"))

        except FileExistsError: ...


    def create_Public_Private(self, key: tuple | None = None, pathForFolder: str | None = None) -> None:
        if key: d, e, n = key
        else: d, e, n = self.load_key(True)
        if not pathForFolder: pathForFolder = os.path.dirname(sys.argv[0])

        self.write_Private(n, d, pathForFolder)
        self.write_Public(n, e, pathForFolder)


    def write_Public(self, n: int, e: int, pathForFolder: str) -> None:
        Publicfile = os.path.join(pathForFolder, "RSA_Geteilt", "PUBLIC", "PUBLIC_Key.txt")
        with open(Publicfile, "w") as Public:
            Public.write(f"Mode: Public\n\n{n}\n{e}\n\n# n, E")
            # Public.write(f"{n}\n{e}\n\n# n, E")
            # Public.write(f"{str(0)}\n{str(0)}\n{str(n)}\n{str(e)}\n{str(0)}\n\n# p, q, n, E, D")
            Public.close()


    def write_Private(self, n: int, d: int, pathForFolder: str) -> None:
        Privatefile = os.path.join(pathForFolder, "RSA_Geteilt", "PRIVATE", "PRIVATE_Key.txt")
        with open(Privatefile, "w") as Private:
            Private.write(f"Mode: Private\n\n{n}\n{d}\n\n# n, D")
            # Private.write(f"{n}\n{d}\n\n# n, D")
            # Private.write(f"{str(0)}\n{str(0)}\n{str(n)}\n{str(0)}\n{str(d)}\n\n# p, q, n, E, D")
            Private.close()


if __name__ == "__main__":
    Split_Keys().create_Public_Private()