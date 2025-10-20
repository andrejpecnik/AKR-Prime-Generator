import random
import os
import math
import timeit
import logging
import time
from cryptography.fernet import Fernet
import base64
import msvcrt


#######################Šifrovanie+Log##############################################
def load_key_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def encrypt_log_file(log_filename, key):
    with open(log_filename, 'rb') as file:
        log_content = file.read()
    cipher = Fernet(key)
    encrypted_content = cipher.encrypt(log_content)
    with open(log_filename, 'wb') as file:
        file.write(encrypted_content)

def decrypt_log_file(log_filename, key):
    with open(log_filename, 'rb') as file:
        encrypted_content = file.read() 
    cipher = Fernet(key)  
    decrypted_content = cipher.decrypt(encrypted_content)  
    with open(log_filename, 'wb') as file:
        file.write(decrypted_content)  

file_path = os.path.join(os.path.dirname(__file__), 'fernet_key.txt')
loaded_key = load_key_from_file(file_path)


def prezeranie_logu():
    while True:
        password = input("Zadajte heslo: ")
        file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
        if password == "tajneheslo":
            decrypt_log_file(file_path, loaded_key)
            print("Stlačte ľubovoľné tlačidlo pre pokračovanie...")
            msvcrt.getch()
            encrypt_log_file(file_path, loaded_key)
            break
        else:
            print("Nesprávne heslo!")

#######################Šifrovanie + Log##############################################

file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
logging.basicConfig(filename=file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

###################### READ WRITE FILE ####################################
def write_list_to_file(lst, filename): #Zapis listu do file
    try:
        with open(filename, 'r'):
            pass
    except FileNotFoundError:
        open(filename, 'w').close()

    with open(filename, 'w') as file:
        for item in lst:
            file.write(str(item) + '\n')

def read_value_from_file():
    while True:
        file_name = input("Zadejte název souboru: ")
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) != 1:
                    print("Chyba - Soubor obsahuje více než jedno řádek")
                else:
                    value = lines[0].strip()
                    if not value.isdigit():
                        print("Chyba - Obsah souboru není celé číslo")
                    else:
                        return int(value)
        except FileNotFoundError:
            print("Chyba - Soubor nenalezen")

def zapis_do_suboru(nazov_suboru, cislo): #Zapis cisla do file
    try:
        file_path = os.path.join(os.path.dirname(__file__), nazov_suboru)
        with open(file_path, "w") as file:
            file.write(str(cislo))  # Zapíšeme dané číslo do súboru
        print(f"Číslo bolo úspešne zapísané do súboru {nazov_suboru}.")
    except Exception as e:
        print(f"Nastala chyba pri zápise do súboru: {e}")
###################### READ WRITE FILE ####################################


######################### Vypis cislo po prvocsilo #####################################

def eratosthenovo_sito(do):
    do += 1
    sito = [True] * do

    for i in range(2, do):
        if sito[i]:
            for j in range(i ** 2, do, i):
                sito[j] = False

    prvocisla = []
    for i in range(2, do):
        if sito[i]:
            prvocisla.append(i)
    return prvocisla

def prvocisloPoCisloRucne():
    #Vypise prvocisla po cislo, ktore je zadane rucne
    zadanePrvocislo = int(input("Zadaj hodnotu cisla po ktore nasledne vypisem vsetky prvocisla: \n"))
    print("ZADANE CISLO:\n"+str(zadanePrvocislo))
    print(eratosthenovo_sito(zadanePrvocislo))
    file_path = os.path.join(os.path.dirname(__file__), 'Eratosthenovo.txt')
    write_list_to_file(eratosthenovo_sito(zadanePrvocislo), file_path)
    print("Vysledok zapisany do Eratosthenovo.txt")

    file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
    decrypt_log_file(file_path, loaded_key)

    duration = timeit.timeit(lambda: eratosthenovo_sito(zadanePrvocislo), number=1)
    logging.info(f'Eratosthenovym sitom vypisane prvocisla, po cislo: {zadanePrvocislo}. \nDoba trvania: {duration:.7f} sekund')


    encrypt_log_file(file_path, loaded_key)

def prvocisloPoCisloImport():
    #Vypise prvocisla po cislo, ktore je zadane importom
    
    zadanePrvocislo = read_value_from_file()
    print("Zadane prvocislo je: \n"+str(zadanePrvocislo)+"\n")
    print(eratosthenovo_sito(zadanePrvocislo))
    file_path = os.path.join(os.path.dirname(__file__), 'Eratosthenovo.txt')
    write_list_to_file(eratosthenovo_sito(zadanePrvocislo), file_path)
    print("Vysledok zapisany do Eratosthenovo.txt")

    file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
    decrypt_log_file(file_path, loaded_key)
    duration = timeit.timeit(lambda: eratosthenovo_sito(zadanePrvocislo), number=1)
    logging.info(f'Eratosthenovym sitom vypisane prvocisla, po cislo: {zadanePrvocislo}. \nDoba trvania: {duration:.7f} sekund ')
    encrypt_log_file(file_path, loaded_key)

def prvocislaPoCislo():
    print("Chcete zadat cislo RUCNE alebo IMPORT zo suboru?")
    vyberAkcie = str(input("RUCNE // IMPORT\n")).lower()

    match vyberAkcie:
        case "rucne":
            prvocisloPoCisloRucne()

        case "import":
            prvocisloPoCisloImport()
        
        case _ :
            print("Nespravny vyber")
            prvocislaPoCislo()
######################### Vypis cislo po prvocislo #####################################

######################### Testovanie #######################################
def miller_rabin(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def je_prvocislo_mr(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(k):
        if not miller_rabin(d, n):
            return False
    return True

def jacobi_symbol(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a % 2 == 0:
        return jacobi_symbol(a // 2, n) * ((-1)**((n**2 - 1) // 8))
    if a >= n:
        return jacobi_symbol(a % n, n)
    if a % 4 == 3 and n % 4 == 3:
        return -jacobi_symbol(n, a)
    return jacobi_symbol(n, a)

def je_prvocislo_ss(n, k=5):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0 or n == 1:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, (n - 1) // 2, n)
        j = jacobi_symbol(a, n)
        if x != 1 and x != 0:
            return False
        if x == 0 or j % n != x % n:
            return False
    return True

def eratostenovo_sito_test():
    yield 2
    primes = [2]
    candidate = 3
    while True:
        is_prime = True
        sqrt_candidate = int(candidate ** 0.5) + 1
        for prime in primes:
            if prime > sqrt_candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
            yield candidate
        candidate += 2


def je_prvocislo_er(n):

    if n <= 1:
        return False, 0.0
    
    start_time = time.time()
    generator = eratostenovo_sito_test()
    while True:
        prime = next(generator)
        if prime > n:
            return False, time.time() - start_time
        if n == prime:
            return True, time.time() - start_time
        if time.time() - start_time > 30:
            print("Eratosthenov test, trval dlhsie ako 30 sekund. Odpoved je irelevantna.")
            return False, 30.0


def testovanie_prvocisla(cislo, k):
    #funkcia na testovanie prvocisla a nasledne zapisanie do logu
    file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
    decrypt_log_file(file_path, loaded_key)

    duration_ss = timeit.timeit(lambda: je_prvocislo_ss(cislo), number=1)
    duration_mr = timeit.timeit(lambda: je_prvocislo_mr(cislo, k), number=1)
    je_prvocislo_er_pravda, trvanie_er = je_prvocislo_er(cislo)

    pocet_bitov = int(math.log2(cislo)) + 1
    
    logging.info(f'Solovay-Strassenov test cisla {cislo}: \nPrvocislo: {je_prvocislo_ss(cislo)}, Doba testovania: {duration_ss:.7f} sekundy, Pocet bitov: {pocet_bitov}')
    logging.info(f'Miller-Rabin test cisla {cislo}: \nPrvocislo: {je_prvocislo_mr(cislo, k)}, Doba testovania: {duration_mr:.7f} sekundy, Pocet bitov: {pocet_bitov}, Pocet iteracii: {k}')
    logging.info(f'Eratosthenovo sito test cisla {cislo}: \nPrvocislo: {je_prvocislo_er_pravda}, Doba testovania: {trvanie_er:.7f} sekundy, Pocet bitov: {pocet_bitov}')
    
    encrypt_log_file(file_path, loaded_key)

    if je_prvocislo_mr(cislo, k):
        print(cislo, "je prvočíslo.")
    else:
        print(cislo, "nie je prvočíslo.")

def testovanie_prvocisla_rucne():
    cislo_k_otestovaniu = int(input("Zadajte číslo k otestovaniu: "))
    pocet_iteraci = int(input("Zadajte počet iterácií: "))
    testovanie_prvocisla(cislo_k_otestovaniu, pocet_iteraci)

def testovanie_prvocisla_import():
    pocet_iteraci = int(input("Zadaj pocet iteracii: "))
    cislo_k_otestovaniu = read_value_from_file()
    print("Zadane prvocislo je: \n"+str(cislo_k_otestovaniu)+"\n")
    testovanie_prvocisla(cislo_k_otestovaniu, pocet_iteraci)

def vyber_moznosti():
    #vyber moznosti pre testovanie prvocisla rucne alebo importom
    print("Chcete zadat cislo RUCNE alebo IMPORT zo suboru?")
    vyberAkcie = str(input("RUCNE // IMPORT\n")).lower()

    match vyberAkcie:
        case "rucne":
            testovanie_prvocisla_rucne()

        case "import":
            testovanie_prvocisla_import()
        
        case _ :
            print("Nespravny vyber")
            prvocislaPoCislo()

######################### Testovanie #######################################


######################### Generovanie ######################################

def miller_rabin(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_mr(bits):
    start_time = time.time()
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1
        if miller_rabin(candidate):
            end_time = time.time()
            duration = end_time - start_time
            return candidate, duration

def modulo_mocnina(a, b, n):
    result = 1
    a = a % n
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % n
        b //= 2
        a = (a * a) % n
    return result

def jacobi_symbol(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 == 3 or n_mod_8 == 5:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

def solovay_strassen_test(n, k=5):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = jacobi_symbol(a, n)
        y = modulo_mocnina(a, (n - 1) // 2, n)
        if x == 0 or y != x % n:
            return False
    return True


def generuj_prvocislo_ss(pocet_bitov):
    start_time = time.time()
    while time.time() - start_time <= 30:
        cislo = random.getrandbits(pocet_bitov)
        if cislo % 2 != 0:
            if solovay_strassen_test(cislo):
                end_time = time.time()
                duration = end_time - start_time
                return cislo, duration
    
    print("Generovanie pomocou SS trvalo dlhsie ako 30 sekund")
    return 0, 30.0

def miller_rabin(n, k=5):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(2, min(1000, n)):
        if n % i == 0:
            return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def lucas_selfridge(n):
    D = 5
    P, Q = 1, (1 - D) // 4

    u, v, k = 0, 2, n

    while k > 0:
        if k & 1:
            u, v = (u * P + v * Q) % n, (v * P + u * Q) % n
        u, v, k = (u * v) % n, (v * v + 2 * (u * u) * Q) % n, k // 2

    if u == 0 or v == 0:
        return True
    else:
        return False

def generuj_prvocislo_ls(bits):
    start_time = time.time()
    while True:
        candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
        if miller_rabin(candidate) and lucas_selfridge(candidate):
            end_time = time.time()
            duration = end_time - start_time
            return candidate, duration

def generujPrvocislo():
    bits = int(input("Zadaj, kolko bitove cislo generujem: "))
    prvocislo_mr, trvanie_mr = generate_prime_mr(bits)
    print("Generované prvočíslo pomocou MR:\n", prvocislo_mr)
    print(trvanie_mr)
    nazov_suboru_mr = "Prvocislo_MR.txt"
    zapis_do_suboru(nazov_suboru_mr, prvocislo_mr)
    prvocislo_ls, trvanie_ls = generuj_prvocislo_ls(bits)
    print("Generované prvočíslo pomocou LS:\n", prvocislo_ls)
    print(trvanie_ls)
    nazov_suboru_ls = "Prvocislo_LS.txt"
    zapis_do_suboru(nazov_suboru_ls, prvocislo_ls)
    prvocislo_ss, trvanie_ss = generuj_prvocislo_ss(bits)
    print("Generované prvočíslo pomocou SS:\n", prvocislo_ss)
    print(trvanie_ss)
    nazov_suboru_ss = "Prvocislo_SS.txt"
    zapis_do_suboru(nazov_suboru_ss, prvocislo_ss)



    file_path = os.path.join(os.path.dirname(__file__), 'test_prvociselnosti.log')
    
    decrypt_log_file(file_path, loaded_key)
    logging.info(f'Solovy-Strassen generator prvocisla:\n {prvocislo_ss}: \nDoba trvania: {trvanie_ss:.7f}, Pocet bitov: {bits}')
    logging.info(f'Miller-Rabinov generator prvocisla:\n {prvocislo_mr}: \nDoba trvania: {trvanie_mr:.7f}, Pocet bitov: {bits}')
    logging.info(f'Lucas-fridge generator prvocisla:\n {prvocislo_ls}: \nDoba trvania: {trvanie_ls:.7f}, Pocet bitov: {bits}')
    encrypt_log_file(file_path, loaded_key)


######################### Generovanie ######################################

#######################             MAIN          ###############################################


#vyber moznosti
def zvolenie():
    while True:
        try:
            print("1..........Vypis vsetkych prvocisel po zadane cislo")
            print("2..........Test prvociselnosti zadaneho prvocisla")
            print("3..........Generovanie velkeho procisla na zaklade zadanej bitovej dlzky")
            print("4..........Prezeranie logu")
            print("5..........UKONCENIE programu!")
            volba = int(input("\nVyber akciu ktoru chces urobit podla cisla: "))
            if volba == 1:
                os.system('cls||clear')
                print("Vypis vsetkych prvocisel po zadane cislo")
                prvocislaPoCislo()
                s = input("Stlacte ENTER")
                os.system('cls||clear')

            elif volba == 2:
                os.system('cls||clear')
                print("Testovanie prvocisla")
                vyber_moznosti()
                s = input("Stlacte ENTER")
                os.system('cls||clear')
                
            elif volba == 3:
                os.system('cls||clear')
                print("Generovanie prvocisla")
                generujPrvocislo()
                s = input("Stlacte ENTER")
                os.system('cls||clear')

            elif volba == 4:
                os.system('cls||clear')
                print("Prezeranie Logu")
                prezeranie_logu()
                os.system('cls||clear')

            elif volba == 5:
                os.system('cls||clear')
                print("Koniec programu")
                s = input("Stlacte ENTER")
                os.system('cls||clear')
                return False

            else:
                print("Musíte zadať 1, 2, 3, 4 alebo 5!")
        except ValueError:
            print("Musíte zadať celé číslo!")


zvolenie()
