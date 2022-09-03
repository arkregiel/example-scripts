# md5_passwd_crack_dict.py
# przykładowy skrypt do łamania haseł
# zahaszowanych algorytmem MD5
# metodą słownikową


#################################################################
#                                                               #
# DISCLAIMER:                                                   #
# Tego skryptu należy używać WYŁĄCZNIE w celach edukacyjnych    #
# i w celu demonstracji metody łamania haseł metodą słownikową. #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań   #
#                                                               #
#################################################################


# Łamanie hasła metodą słownikową polega na tworzeniu hashy danych
# z wcześniej przygotowanej listy słów i porównywaniu ich
# z hashem hasła, które chcemy poznać. Dzieje się tak dlatego,
# ponieważ hashowanie jest funkcją jednokierunkową, tzn. nie powinno być
# możliwe obliczenie wartości danych na podstawie ich hasha.
# Łamanie hasła jest więc niejako jego zgadywaniem.
# Oczywiście musimy mieć hash hasła, żeby móc go złamać.
# Przykładowo hash MD5 słowa secret to 5ebe2294ecd0e0f08eab7690d2a6ee69,
# hash MD5 słowa password to 5f4dcc3b5aa765d61d8327deb882cf99,
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

# Lista argv zawiera argumetny wiersza poleceń,
# z jakimi został uruchomiony skrypt.
from sys import argv

# Przykładowy słownik, z którego skorzystamy do łamania hasła.
# Często takie słowniki to pliki tekstowe zawierające
# setki, tysiące czy nawet miliony słów i ciągów znaków.
# Przykładowy słownik zawierający miliony
# popularnych haseł nazywa się rockyou.txt
wordlist = (
    '1234',
    'admin',
    'secret',
    'password'
)

# Skrypt jest uruchamiany wraz z wartością haszu MD5 hasła,
# które będziemy próbować złamać.
# Pierwszy element listy argv (o indeksie 0) to nazwa skryptu,
# dlatego jej długość powinna wynosić 2 (drugi element to hash MD5)
if len(argv) < 2:

    # Jeśli skrypt zostanie uruchomiony bez hasha,
    # wypisuje sposób użycia, przykład i kończy działanie
    print(f"sposób użycia: python {argv[0]} <hasz md5>")
    print(f"przykład: python {argv[0]} 5ebe2294ecd0e0f08eab7690d2a6ee69")
    quit()

# pobieramy wartość hasza z listy argv
password_hash = argv[1]

# Przystępujemy do próby złamania hasła.
# Dla każdego słowa ze słownika utworzymy jego hash
# i porównamy go z podanym hashem hasła
for word in wordlist:

    # Tworzymy obiekt, którego użyjemy do 
    # utworzenia hasha słowa ze słownika
    hash_obj = md5()

    # Obiekt hash_obj operuje na bajtach,
    # dlatego konwertujemy wartość word
    # z tekstu na bajty używając kodowania UTF-8
    word_bytes = bytes(word, encoding='utf-8')

    # Dodajemy dane do obiektu haszującego
    hash_obj.update(word_bytes)

    # Obliczamy hash słowa ze słownika
    # i zwracamy go w postaci zrzutu szesnastkowego,
    # czyli ciągu znaków skłaającego się z cyfr szesnastkowych (0-9 i A-F),
    # który reprezentuje wartość hasha
    word_hash = hash_obj.hexdigest()

    # Porównujemy hash słowa ze słownika z hashem łamanego hasła
    if word_hash == password_hash:

        # Jeśli hashe są równe, złamaliśmy hasło.
        # Wypisujemy złamane hasło i przerywamy pętlę
        # kończąc działanie skryptu
        print("Złamano hasło!")

        # Wypisujemy słowo, którego hash MD5 odpowiada
        # hashowi łamanwgo hasła
        print("Hasło: " + word)
        break

# Jeśli nie udało się złamać hasła (hasło nie znajdowało się w słowniku),
# wypisujemy informację o nieudanej próbie łamania hasła
else:
    print("Nie udało się złamać hasła")
