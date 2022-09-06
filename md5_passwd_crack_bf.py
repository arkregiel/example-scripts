# md5_passwd_crack_bf.py
# przykładowy skrypt do łamania haseł
# zahaszowanych algorytmem MD5
# metodą siłową (brute force)

#################################################################
#                                                               #
# DISCLAIMER:                                                   #
# Tego skryptu należy używać WYŁĄCZNIE w celach edukacyjnych    #
# i w celu demonstracji metody łamania haseł metodą siłową.     #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań   #
#                                                               #
#################################################################

# Łamanie hasła metodą siłową polega na tworzeniu hashy ciągów znaków
# utworzonych w procesie generowania wariacji (z powtórzeniami) elementów
# ze zbioru znaków i podanej długości, a następnie porównywaniu ich
# z hashem hasła, które chcemy poznać. Dzieje się tak dlatego,
# ponieważ hashowanie jest funkcją jednokierunkową, tzn. nie powinno być
# możliwe obliczenie wartości danych na podstawie ich hasha.
# Łamanie hasła jest więc niejako jego zgadywaniem i może zająć
# bardzo dużo czasu.Oczywiście musimy mieć hash hasła, żeby móc go złamać.
# Przykładowo hash MD5 słowa secret to 5ebe2294ecd0e0f08eab7690d2a6ee69,
# hash MD5 ciągu znaków 123 to 202cb962ac59075b964b07152d234b70,
# a hash MD5 słowa secret1 to e52d98c459819a11775936d8dfbb7929.
# Ten skrypt jest proof-of-concept, w realnych warunkach łamanie hasła
# może (jednak nie musi!) zająć sporo czasu. Dlatego ważne jest używanie
# silnych haseł: minimum 8 znaków, małe i wielkie litery,
# cyfry oraz znaki specjalne.

# Z biblioteki importujemy funkcjonalność
# zapewniającą obliczanie hashy MD5.
# Więcej informacji na temat biblioteki hashlib na stronie:
# https://docs.python.org/3/library/hashlib.html
from hashlib import md5

# Z tej biblioteki skorzystamy do wygenerowania
# wariacji ciągów znaków, których użyjemy
# w próbie łamania hasła
# https://docs.python.org/3/library/itertools.html
import itertools

# Lista argv zawiera argumetny wiersza poleceń,
# z jakimi został uruchomiony skrypt.
from sys import argv

# Z tego modułu skorzystamy, żeby nie pisać ręcznie 
# wszystkich 95 znaków, których będziemy używać
# przy łamaniu hasła
import string

# Tworzymy zbiór znaków, których użyjemy do generowania
# ciagów znaków będących próbami odgadnięcia hasła
ALPHABET = string.ascii_letters + string.digits 
ALPHABET += r"~`!@#$%^ &*()-_=+[]{}|\';:,.<>/?" + '"'  # 95 znaków

# Skrypt jest uruchamiany wraz z wartością hasha MD5 hasła,
# które będziemy próbować złamać.
# Pierwszy element listy argv (o indeksie 0) to nazwa skryptu,
# dlatego jej długość powinna wynosić 2 (drugi element to hash MD5)
if len(argv) < 2:

    # Jeśli skrypt zostanie uruchomiony bez hasha,
    # wypisuje sposób użycia, przykład i kończy działanie
    print(f"sposób użycia: python {argv[0]} <hasz md5>")
    print(f"przykład: python {argv[0]} 202cb962ac59075b964b07152d234b70")
    quit()

# pobieramy wartość hasha z listy argv
password_hash = argv[1]

# Przystępujemy do próby łamania hasła
print("Łamanie hasła...")

# Sprawdzimy wszyskie ciągi znaków utworzonych z zawartości zmiennej ALPHABET
# o długościach od 1 do 16.
# Już dla ciągu znaków o długości 4 ten skrypt nie da odpowiedzi aż tak szybko
for length in range(1, 17):

    print("Sprawdzanie ciągów znaków o długości: " + str(length))

    # Korzystamy z funkcji itertools.product do wygenerowania wariacji
    # ciągów znaków o danej długości length.
    # Dla ciągu znaków o długości 5 jest ich 95^5 (mamy do dyspozycji 95 znaków)
    for variation in itertools.product(ALPHABET, repeat=length):

        # Funkcja itertools.product zwraca krotkę,
        # dlatego zamieniamy zmienną variation na tekst
        # łącząc znaki w krotce
        variation = ''.join(variation)

        # Tworzymy obiekt, którego użyjemy do 
        # utworzenia hasha sprawdzanego ciągu znaków
        hasher = md5()

        # Obiekt hasher operuje na bajtach,
        # dlatego konwertujemy wartość zmiennej variation
        # z tekstu na bajty używając kodowania UTF-8
        guess = bytes(variation, encoding='utf-8')
        
        # Dodajemy dane do obiektu haszującego
        hasher.update(guess)

        # Obliczamy hash sprawdzanego ciągu znaków
        # i zwracamy go w postaci zrzutu szesnastkowego,
        # czyli ciągu znaków skłaającego się z cyfr szesnastkowych (0-9 i A-F),
        # który reprezentuje wartość hasha
        guess_hash = hasher.hexdigest()

        # Porównujemy hash sprawdzanego ciągu znaków z hashem łamanego hasła
        if guess_hash == password_hash:

            # Jeśli hashe są równe, złamaliśmy hasło.
            # Wypisujemy złamane hasło i przerywamy pętlę
            # kończąc działanie skryptu
            print("Złamano hasło!")

            # Wypisujemy słowo, którego hash MD5 odpowiada
            # hashowi łamanwgo hasła
            print("Hasło: " + variation)
            quit()

# Jeśli nie udało się złamać hasła (hasło nie znajdowało się w słowniku),
# wypisujemy informację o nieudanej próbie łamania hasła
else:
    print("Nie udało się złamać hasła")
