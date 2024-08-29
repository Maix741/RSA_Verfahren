from RSA_Key_split import create_Public_Private
import random, os, sys
import time


def get_p_q() -> int:
    """get p, q"""
    Start, Ende = input("Start Prim: "), input("Ende Prim: ")
    try:
        Start, Ende = int(Start), int(Ende)
    except ValueError:
        return 0, 0
    primzahlen = get_Primzahlen(Start, Ende)
    while True:
        p, q = random.choice(primzahlen), random.choice(primzahlen)
        if q != p:
            primzahlen.clear()
            print("p und q generiert!")
            return p, q


def generate_Keys() -> int:
    p, q = get_p_q()

    n = p * q
    m = (p - 1) * (q - 1)

    # get E, D
    E = get_E(m)
    D = get_D(m, E)

    # p, q, n, D ,E, m = 2, 11, 22, 7, 3, 10

    return p, q, n, E, D


def get_E(m: int, e: int = 0) -> int:
    Start_E = int(input("Start_E: "))
    e = Start_E
    while m % e == 0:
        if e >= m:
            print("Error")
            return None
        e += 1

    print("E generiert!")
    return e


def get_D(m: int, E: int, d: int = 1) -> int:
    # d = int(m/2)
    try:
        while (E * d % m) != 1:
            d += 1
    except KeyboardInterrupt:
        print("Error: ", d)
        return None
    print("D generiert!")
    return d

def get_Primzahlen(Start: int, Ende: int) -> list:
    """alle primzahlen in Bereich ausgeben"""

    primzahlen = []
    for zahl in range(Start, Ende):
        teilbar = False
        if zahl > 1:
            for primzahl in primzahlen:
                if teilbar:
                    break
                if zahl % primzahl == 0:
                    teilbar = True

            if not teilbar:
                primzahlen.append(zahl)

    return primzahlen


def write_Keys(p: int, q: int, n: int, E: int, D: int) -> None:
    with open(os.path.realpath(os.path.realpath(os.path.dirname(sys.argv[0]))) + "/KEYS//RSA_Key.txt", "w") as KEYS_Datei:
        KEYS_Datei.truncate()
        # KEYS_Datei.write(f"{str(p)}\n{str(q)}\n{str(n)}\n{str(E)}\n{str(D)}\n\n# erst p, q, n, E, D")
        KEYS_Datei.write(str(p) + "\n")
        KEYS_Datei.write(str(q) + "\n")
        KEYS_Datei.write(str(n) + "\n")
        KEYS_Datei.write(str(E) + "\n")
        KEYS_Datei.write(str(D) + "\n\n")
        KEYS_Datei.write("# erst p, q, n, E, D")
        KEYS_Datei.close()


if __name__ == "__main__":
    Start = time.time()
    p, q, n, E, D = generate_Keys()
    print(f"p, q, n, E, D: {p, q, n, E, D}")
    print(time.time() - Start)
    if input("Datei erstellen(y/n): ").lower().replace(" ", "") == "y":
        write_Keys(p, q, n, E, D)
        create_Public_Private()


# Geschwindigkeit Primzahlen:
    # 1-999999 -> 163.43349385261536 Sekunden --> 78498 Primzahlen