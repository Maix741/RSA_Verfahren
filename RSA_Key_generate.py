from colorama import Fore, Style
from decimal import Decimal
import os, sys
import random


class Generate_Keys:
    def __init__(self) -> None:
        self.currentDir = os.path.dirname(sys.argv[0])
        try:
            os.mkdir(os.path.join(self.currentDir, "KEYS"))
        except FileExistsError: ...


    def is_prime(self, number: int) -> bool:
        if number <= 2:
            return False
        number == Decimal(number)
        for i in range(2, int(number ** Decimal(0.5)) + 1):
            if number % i == 0:
                return False
        return True


    def generate_random_prime(self, start: int, end: int) -> int:
        while True:
            num = random.randint(start, end)
            if self.is_prime(num):
                return num


    def gcd(self, a: int, b: int) -> int:
        while b != 0:
            a, b = b, a % b

        return a


    def multiplicative_inverse(self, e: int, m: int) -> int | None:
        def extended_gcd(a: int, b: int) -> int:
            if a == 0:
                return b, 0, 1

            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

        gcd, x, _ = extended_gcd(e, m)
        if gcd != 1:
            return None

        return x % m


    def generate_E(self, m: int) -> int:
        e = random.randrange(1, m)
        while self.gcd(e, m) != 1:
            e = random.randrange(1, m)
        print(f"{Fore.GREEN}E generiert!{Style.RESET_ALL}")
        return e


    def generate_keypair(self, p: int, q: int) -> tuple:
        n = p * q
        m = (p - 1) * (q - 1)


        e = self.generate_E(m)
        d = self.multiplicative_inverse(e, m)

        if not d:
            raise ValueError('Failed to generate proper RSA key pair')
        print(f"{Fore.GREEN}D generiert!{Style.RESET_ALL}")

        return (p, q, n, e, d)


    def generate_keys(self, minEnde: int = 100000) -> tuple:
        Ende = minEnde - 1
        for _ in range(10):
            try:
                Ende = int(input(f"Geben sie das Ende der Primzahlsuche ein(min: {minEnde}): "))
                break

            except ValueError:
                print(f"{Fore.RED}Bitte geben sie eine Zahl ein!{Style.RESET_ALL}")

        if Ende < minEnde:
            Ende += minEnde

        validKeyPair = False
        while not validKeyPair:
            p = self.generate_random_prime(Ende - minEnde, Ende)
            q = self.generate_random_prime(Ende - minEnde, Ende)
            while p == q:
                p = self.generate_random_prime(Ende - minEnde, Ende)
                q = self.generate_random_prime(Ende - minEnde, Ende)

            print(f"{Fore.GREEN}p, q generiert!{Style.RESET_ALL}")

            try:
                key = self.generate_keypair(p, q)
                validKeyPair = True
            except ValueError:
                print(f"{Fore.RED}Es gab einen Fehler beim generieren des Schlüssels!{Style.RESET_ALL}")
                print(f"{Fore.RED}Wiederhole Generierung...{Style.RESET_ALL}")
                validKeyPair = False

        return key


    def write_Keys(self, key: tuple[int], keyDirectory: str | None = None) -> str:
        rootDir = keyDirectory if keyDirectory else self.currentDir
        p, q, n, e, d = key
        file = os.path.join(rootDir, "KEYS", "RSA_Key.key")
        i = 1
        while os.path.isfile(file):
            file = os.path.join(rootDir, "KEYS", f"RSA_Key{i}.key")
            i += 1
        with open(file, "w") as Keys_Datei:
            Keys_Datei.write(f"{str(p)}\n{str(q)}\n{str(n)}\n{str(e)}\n{str(d)}\n\n# p, q, n, E, D")
            Keys_Datei.close()
        return file


if __name__ == "__main__":
    Generator = Generate_Keys()
    key = Generator.generate_keys(minEnde=999999)
    print(f"{Fore.GREEN}Schlüssel erfolgreich generiert!{Style.RESET_ALL}")
    print(f"p, q, n, E, D: {key}")
    if input("Datei erstellen(y/n): ") == "y":
        Generator.write_Keys(key)
        if input("Schlüssel teilen?(y/n): ") == "y":
            from RSA_Key_split import Split_Keys
            Split_Keys().create_Public_Private(key)