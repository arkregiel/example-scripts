# hash_checksum.py
# wypisuje wartość funkcji skrótu (hash) dla pliku lub wpisanych danych
# obsługiwane algorytmy: MD4, SHA256, SHA512

# Twórcy oprogramowania często udostępniają również sumę kontrolną pliku,
# która jest wartością funkcji haszującej (np. MD5 lub SHA256),
# dzięki której użytkownik może sprawdzić integralność pliku,
# czyli, czy plik nie został zmodyfikowany przez kogoś o nieetycznych intencjach.
# Użytkownik może sam obliczyć wartość hasz dla pliku i porównać
# z wartością udostępnioną przez twórców oprogramowania.
# Ten skrypt zapewnia taką funkcjonalnośc

# ta biblioteka udostępnia funkcje haszujące
# więcej informacji na jej temat na stronie:
# https://docs.python.org/3/library/hashlib.html
import hashlib

# lista argv zawiera argumetny wiersza poleceń,
# z jakimi został uruchomiony skrypt
from sys import argv

# krotka zawierająca nazwy algorytmów wspieranych przez skrypt
wspierane_algorytmy = ('md5', 'sha256', 'sha512')

# Skrypt jest uruchamiany z nazwą algorytmu haszującego (obowiązkowo)
# i nazwą pliku, który zostanie poddany haszowaniu (opcjonalnie).
# Pierwszy element listy argv (o indeksie 0) to nazwa skryptu,
# dlatego jej długość powinna wynosić 2 (drugi element to nazwa algorytmu)
if len(argv) < 2:

    # Jeśli skrypt zostanie uruchomiony bez nazwy funkcji haszującej,
    # wypisuje sposób użycia, przykłady i kończy działanie
    print("sposób użycia: python hash_checksum.py <algorytm> [nazwa pliku]")
    print("przykłady:")
    print("$ python hash_checksum.py sha256 plik.txt")
    print("$ python hash_checksum.py sha256")
    quit()

# Pobieramy nazwę algorytmu haszującego z listy argv
algorytm = argv[1]

# Jeśli nazwa algorytmu nie widnieje w krotce obsługiwanych algorytmów,
# skrypt wypisuje, jakie algorytmy wspiera i kończy działanie
if algorytm not in wspierane_algorytmy:
    print("Program wspiera algorytmy: md5, sha256, sha512")
    quit()

# Tworzymy obiekt haszujący z nazwą wybranego algorytmu.
# Użyjemy go do obliczenia wartości funkcji skrótu
hasz = hashlib.new(algorytm)

# Tryb 1: skrypt został uruchomiony wraz z nazwą pliku.
if len(argv) == 3:

    # pobranie nazwy pliku z listy argv
    nazwa_pliku = argv[2]

    # W przypadku pracy z plikami, spodziewamy się,
    # że może wystąpić błąd, 
    # plik może na przykład nie istnieć
    try:

        # Otwieramy plik o podanej nazwie w trybie binarnego odczytu.
        # Dzięki temu skrypt obliczy funkcję skrótu również dla pliku,
        # który nie jest plikiem tekstowym
        # Korzystając z konstrukcji with, nie przejmujemy się zamknięciem pliku,
        # konstrukcja with zrobi to za nas
        with open(nazwa_pliku, 'rb') as plik:

            # Wczytujemy dane z pliku do zmiennej
            dane = plik.read()

            # Dodajemy dane do obiektu haszującego
            hasz.update(dane)
    except OSError as err:

        # W przypadku wystąpienia błędu, wypisujemy stosowny komunikat
        # i informację o błędzie, po czym skrypt kończy działanie.
        print("Nie udało się otworzyć pliku")
        print(err)
        quit()

# Tryb 2: skrypt został uruchomiony bez nazwy pliku
# W tym przypadku wypiszemy hasz dla danych podanych z klawiatury
else:

    # Prosimy użytkownika o wpisanie danych
    print("Wpisz dane:")

    # Wypisujemy znak zachęty (">") i pobieramy dane z klawiatury
    dane = input("> ")

    # Funkcja input() zwraca tekst, natomiast
    # metoda update() przyjmuje bajty jako argument,
    # dlatego konwertujemy dane z tekstu na bajty używając kodowania UTF-8
    dane = bytes(dane, encoding='utf-8')

    # Dodajemy dane do obiektu haszującego
    hasz.update(dane)

# pobieramy wartość skrótu w postaci zrzutu szesnastkowego,
# czyli ciągu znaków skłaającego się z cyfr szesnastkowych (0-9 i A-F),
# który reprezentuje wartość funkcji haszującej
checksum = hasz.hexdigest()

# Wypisujemy nazwę algorytmu wielkimi literami
# oraz wartość skrótu oddzielone dwukropkiem i spacją
print(algorytm.upper(), checksum, sep=": ")
