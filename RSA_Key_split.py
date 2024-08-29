import os, sys


def create_Folder_structure(current_dir: str) -> None:
    try:
        os.mkdir(fr"{current_dir}\RSA_Geteilt")
        os.mkdir(fr"{current_dir}\RSA_Geteilt\PUBLIC")
        os.mkdir(fr"{current_dir}\RSA_Geteilt\PRIVATE")
    
    except FileExistsError:
        print("Ordner bereits erstellt.")


def create_Public_Private() -> None:
    os.chdir(os.path.dirname(sys.argv[0]))
    current_dir = os.getcwd()
    create_Folder_structure(current_dir)
    Keys = []
    with open(f"{current_dir}\KEYS\RSA_KEY.txt", "r") as Keys_Datei:
        for line in Keys_Datei.readlines():
            Keys.append(line.rstrip())  # erst p, q, n, E, D
        Keys_Datei.close()

    n, E, D = Keys[2], Keys[3], Keys[4]

    write_Privat(n, D, current_dir)
    write_Public(n, E, current_dir)


def write_Public(n: int, E: int, current_dir: str) -> None:
    with open(fr"{current_dir}\RSA_Geteilt\PUBLIC\PUBLIC_Key.txt", "w") as Public:
        Public.write(f"{n}\n{E}\n\n# erst n, E")
        Public.close()


def write_Privat(n: int, D: int, current_dir: str) -> None:
    with open(fr"{current_dir}\RSA_Geteilt\PRIVATE\PRIVATE_Key.txt", "w") as Private:
        Private.write(f"{n}\n{D}\n\n# erst n, E")
        Private.close()


if __name__ == "__main__":
    try:
        create_Public_Private()
    except Exception as error:
        print("Error: {error}".format(error))