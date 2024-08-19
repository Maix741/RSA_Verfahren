import os, sys


def create_Public_Private():
    KEYS = []
    os.chdir(os.path.dirname(sys.argv[0]))
    if not str(os.getcwd()).endswith("RSA_Verfahren"):
        os.chdir("../")
    with open((os.getcwd() + "/KEYS//RSA_Key.txt"), "r") as Keys_Datei:
        for line in Keys_Datei.readlines():
            KEYS.append(line.rstrip())  # erst p, q, n, E, D
    
    _, _, n, E, D = KEYS[0], KEYS[1], KEYS[2], KEYS[3], KEYS[4]

    write_Privat(n, D)
    write_Public(n, E)


def write_Public(n: int, E: int) -> None:
    if str(os.path.dirname(sys.argv[0])).endswith("RSA_Geteilt"):
        with open(os.path.dirname(sys.argv[0]) + "/PUBLIC/RSA_Key_PUBLIC.txt", "w") as Public:
            Public.truncate()
            Public.write(str(n) + "\n" + str(E) + "\n" + "\n" + "# erst n, E")
            Public.close()


    elif str(os.path.dirname(sys.argv[0])).endswith("RSA_Verfahren"):
        with open(os.path.dirname(sys.argv[0]) + "/RSA_Geteilt/PUBLIC/RSA_Key_PUBLIC.txt", "w") as Public:
            Public.truncate()
            Public.write(str(n) + "\n" + str(E) + "\n" + "\n" + "# erst n, E")
            Public.close()


def write_Privat(n: int, D: int) -> None:
    if str(os.path.dirname(sys.argv[0])).endswith("RSA_Geteilt"):
        with open(os.path.dirname(sys.argv[0]) + "/PRIVATE/RSA_Key_PRIVATE.txt", "w") as Private:
            Private.truncate()
            Private.write(str(n) + "\n" + str(D) + "\n" + "\n" + "# erst n, D")
            Private.close()


    elif str(os.path.dirname(sys.argv[0])).endswith("RSA_Verfahren"):
        with open(os.path.dirname(sys.argv[0]) + "/RSA_Geteilt/PRIVATE/RSA_Key_PRIVATE.txt", "w") as Private:
            Private.truncate()
            Private.write(str(n) + "\n" + str(D) + "\n" + "\n" + "# erst n, D")
            Private.close()


if __name__ == "__main__":
    try:
        create_Public_Private()
    except ValueError and FileNotFoundError and FileExistsError:
        print("Error")