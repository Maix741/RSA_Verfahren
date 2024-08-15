import random
import time

def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
    return prime_list


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

Start_time = time.time()
prime_list = primesInRange(1, 1000)
randomPrime = random.choice(prime_list)

print("Generated random prime number: ", randomPrime)
Zeit1 = (time.time()) - Start_time

Start_time2 = time.time()
prime_list = get_Primzahlen(1, 1000)
randomPrime = random.choice(prime_list)

print("Generated random prime number: ", randomPrime)
Zeit2 = (time.time()) - Start_time2



print(f"Zeiten: {Zeit1}, {Zeit2}")