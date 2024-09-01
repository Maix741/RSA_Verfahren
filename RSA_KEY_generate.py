import os, sys
import random
import time


class Generate_Keys:
    def __init__(self) -> None:
        currentDir = os.path.dirname(sys.argv[0])
        os.chdir(currentDir)
        try:
            os.mkdir(os.path.join(currentDir, "KEYS"))
        except FileExistsError:
            pass


    def generate_keys(self) -> tuple:
        p, q = self.get_p_q()

        n = p * q
        m = (p - 1) * (q - 1)

        e = self.get_E(m)
        d = self.get_D(m, e)

        return p, q, n, e, d


    def get_p_q(self) -> int:
        """get p, q"""
        Ende = 1
        minEnde = 10000
        for _ in range(10):
            try:
                Ende = int(input(f"Geben sie das Ende der Primzahlsuche ein(min: {minEnde}): "))
                break
            except ValueError:
                print("Bitte geben sie eine Zahl ein!")
                continue

        if Ende < minEnde:
            Ende += minEnde

        primzahlen = self.get_Primzahlen(Ende - minEnde, Ende)

        p, q = 1, 2
        while p == q or p <= 1 or q <= 1:
            p, q = random.choice(primzahlen), random.choice(primzahlen)

        primzahlen.clear()
        print("p und q generiert!")
        return p, q


    def get_E(self, m: int, e: int = 2) -> int:
        for _ in range(10):
            try:
                e = int(input("Geben sie den Start der Suche Nach E ein: "))
                break
            except ValueError:
                print("Bitte geben sie eine Zahl ein!")
                continue

        while m % e == 0:
            if e >= m:
                print("Error")
                return None
            e += 1

        print("E generiert!")
        return e


    def get_D(self, m: int, e: int, d: int = 1) -> int:
        # d = int(m/2)
        try:
            while (e * d % m) != 1:
                d += 1
        except KeyboardInterrupt:
            print("KeyboardInterrupt(D): ", d)
            return None
        print("D generiert!")
        return d


    def get_Primzahlen(self, Start: int, Ende: int) -> list:
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


    def write_Keys(self, p: int, q: int, n: int, e: int, d: int) -> None:
        fileDir = fr"{os.getcwd()}\KEYS\RSA_Key.txt"
        i = 1
        while os.path.isfile(fileDir):
            fileDir = fr"{os.getcwd()}\KEYS\RSA_Key" + str(i) +".txt"
            i += 1
        with open(fileDir, "w") as Keys_Datei:
            Keys_Datei.write(f"{str(p)}\n{str(q)}\n{str(n)}\n{str(e)}\n{str(d)}\n\n# erst p, q, n, E, D")
            Keys_Datei.close()


if __name__ == "__main__":
    Start = time.time()
    Generator = Generate_Keys()
    p, q, n, E, D = Generator.generate_keys()
    print(f"p, q, n, E, D: {p, q, n, E, D}")
    print(time.time() - Start)
    if input("Datei erstellen(y/n): ") == "y":
        Generator.write_Keys(p, q, n, E, D)
        if input("Split Key?(y/n): ") == "y":
            from RSA_Key_split import Split_Keys
            Split_Keys().create_Public_Private()



# Geschwindigkeit Primzahlen:
    # 1-999999 -> 163.43349385261536 Sekunden --> 78498 Primzahlen