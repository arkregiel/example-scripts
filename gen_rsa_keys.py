# gen_rsa_keys.py
# proste generowanie par kluczy RSA

# Ta biblioteka pozwala na wykonywanie
# operacji kryptograficznych takich jak
# szyfrowanie, odszyfrowywanie, generowanie
# kluczy etc.
# https://pycryptodome.readthedocs.io/en/latest/
# Można ją zainstalować poleceniem
# pip install pycryptodome
from Crypto.PublicKey import RSA

# funkcja getpass pozwala na bezpieczne
# wpisanie hasła przez użytkownika
# (nie widać wpisywanych znaków)
from getpass import getpass

# Pobieramy od użytkownika hasło do zaszyfrowania klucza prywatnego
passphrase = getpass("Podaj hasło dla klucza prywatnego: ")

print("Generowanie pary kluczy RSA (2048 bitów)...")

# Generujemy parę kluczy RSA
key_pair = RSA.generate(2048)

# Eksportujemy klucze w formacie PEM
public_key = key_pair.publickey().export_key("PEM")  # bytes
private_key = key_pair.exportKey("PEM", passphrase=passphrase)  # bytes

# Wypisujemy klucze na ekran
print("Klucz publiczny:")
print(public_key.decode())

print("Klucz prywatny:")
print(private_key.decode())