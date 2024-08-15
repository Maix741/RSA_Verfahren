import random, os, sys
# from RSA_Geteilt.RSA_Key_split import create_Public_Private

def get_p_q() -> int:
    # get p, q
    Start, Ende = input("Start Prim: "), input("Ende Prim: ")
    try:
        Start, Ende = int(Start), int(Ende)
    except ValueError:
        return 0, 0
    primzahlen = get_Primzahlen(Start, Ende)
    Primzahlen_richtig = False
    while not Primzahlen_richtig:
        p, q = random.choice(primzahlen), random.choice(primzahlen)
        if q != p:
            Primzahlen_richtig = True
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


def get_E(m: int) -> int:
    Start_E = int(input("Start_E: "))
    for i in range(Start_E, (Start_E + 100)):
        if i <= 1 or i >= m:
            return None
        elif m % i != 0:
            return i


def get_D(m: int, E: int) -> int:
    D = 0
    while D < 9999999999:
        D += 1
        if (E * D) % m == 1:
            return D
    return D


def get_Primzahlen(Start: int, Ende: int) -> list:
    # alle primzahlen in Bereich ausgeben

    zahlen = list(range(Start, Ende))
    primzahlen = []

    for zahl in zahlen:
        teilbar = False
        if zahl > 1:
            for primzahl in primzahlen:
                if zahl % primzahl == 0:
                    teilbar = True
                else:
                    pass
            if not teilbar:
                primzahlen.append(zahl)

    return primzahlen


def write_Keys(p: int, q: int, n: int, E: int, D: int) -> None:
    with open(os.path.realpath(os.path.realpath(os.path.dirname(sys.argv[0]))) + "/KEYS//RSA_KEY.txt", "w") as KEYS_Datei:
        KEYS_Datei.truncate()
        # KEYS_Datei.write(str(p) + "\n" + str(q) + "\n" + str(n) + "\n" + str(E) + "\n" + str(D) + "\n" + "\n" + "# erst p, q, n, E, D")
        KEYS_Datei.write(str(p) + "\n")
        KEYS_Datei.write(str(q) + "\n")
        KEYS_Datei.write(str(n) + "\n")
        KEYS_Datei.write(str(E) + "\n")
        KEYS_Datei.write(str(D) + "\n" + "\n")
        KEYS_Datei.write("# erst p, q, n, E, D")
        KEYS_Datei.close()


def ggT(a: int, b: int) -> int:
    # print("New *a* is " + str(a) + ", new *b* is " + str(b))
    # print(f"b {b}")
    if b == 0:
        # print("b is 0, stopping recursion, a is the ggT: " + str(a))
        return a, b
    # print("Recursing with new a = b and new b = a % b...")
    return ggT(b, a % b)


if __name__ == "__main__":
    p, q, n, E, D = generate_Keys()
    print(f"p, q, n, E, D: {p, q, n, E, D}")
    if input("Datei erstellen(y/n): ").lower().replace(" ", "") == "y":
        write_Keys(p, q, n, E, D)
        # create_Public_Private()