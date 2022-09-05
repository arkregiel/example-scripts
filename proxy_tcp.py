# proxy_tcp.py
# Prosty serwer pośredniczący TCP.
# odbiera połączenie od klienta a następnie łączy się
# z podanym hostem i przekazuje dane wymieniane
# między nimi

#################################################################
# DISCLAIMER:                                                   #
# Skrypt może potencjalnie posłużyć do przechwycenia            #
# wrażliwych informacji. NIE NALEŻY przechwytywać ruchu         #
# innych osób bez ich wiedzy i wyraźnej zgody.                  #
# (artykuły 267 oraz 269b Kodeksu karnego).                     #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań.  #
#################################################################

# Skrypt jest uruchamiany z trzema argumentami:
# Skrypt uruchamiamy z 3 argumentami:
# - numerem portu, na którym ma działać serwer,
# - nazwą hosta, z którym proxy ma się połączyć,
# - numer portu zdalnego hosta, z którym proxy ma się połączyć.
# Po otrzymaniu połączenia od klienta, skrypt
# łączy się ze zdalnym hostem.
# Dane odebrane od klienta przekazywane są
# zdalnemu rozmówcy, a dane odebrane od zdalengo
# rozmówcy zostają wysłane do klienta.

# ta biblioteka jest potrzebna do przeprowadzania operacji sieciowych
import socket

# moduł zawierający funkcje
# ułatwiające pracę z wieloma gniazdami
# jednocześnie (tzw. zwielokrotnione I/O)
# https://docs.python.org/3/library/select.html
import select

# Lista argv zawiera argumetny wiersza poleceń,
# z jakimi został uruchomiony skrypt.
from sys import argv

# Funkcja hexlify z modułu binascii
# tworzy szesnastkową reprezentację
# binarnych danych.
# Skorzystamy z niej przy tworzeniu
# zrzutu szesnastkowego odebranych danych
# https://docs.python.org/3/library/binascii.html
from binascii import hexlify

# Moduł pozwalający na korzystanie
# z wyrażeń regularnych.
# Skorzystamy z niego tworząc zrzut szesnastkowy
# https://docs.python.org/3/library/re.html
import re

# Funkcja tworząca zrzut szesnastkowy
# odebranych binarnych danych
def hexdump(buffer):
    hxdmp = []
    for i in range(0, len(buffer), 16):
        row = hexlify(buffer[i:i + 16], b' ').decode()
        padding = 48 - len(row) if len(row) < 48 else 0

        # Zastępujemy "niedrukowalne" znaki kropką (.)
        row += ' ' * padding + ' ' + re.sub(rb'[^ -~]', b'.', buffer[i:i + 16]).decode()
        hxdmp.append(row)
    hxdmp = '\n'.join(hxdmp)
    return hxdmp

# Skrypt uruchamiamy z 3 argumentami:
# - numerem portu, na którym ma działać serwer,
# - nazwą hosta, z którym proxy ma się połączyć,
# - numer portu zdalnego hosta, z którym proxy ma się połączyć.
# Pierwszy element listy argv (o indeksie 0) to nazwa skryptu,
# dlatego jej długość powinna wynosić 4
if len(argv) < 4:

    # Jeśli skrypt zostanie uruchomiony bez wymaganych argumentów,
    # wypisuje sposób użycia, przykład i kończy działanie
    print(f"sposób użycia: python {argv[0]} <local port> <remote host> <remote port>")
    print(f"przykład: python {argv[0]} 8080 localhost 8888")
    quit()

# Pobieramy z argv numer portu,
# na którym będzie działał serwer
# i konwertujemy go z tekstu na int
bind_port = int(argv[1])

# Pobieramy z argv nazwę hosta,
# z którym serwer ma się połączyć
# po otrzymaniu połączenia od klienta
remote_host = argv[2]

# Pobieramy z argv numer portu,
# z którym serwer ma się połączyć
# po otrzymaniu połączenia od klienta
# i konwertujemy go z tekstu na int
remote_port = int(argv[3])

# wykorzystanie bloku try-except oznaczaz
# że spodziewamy się wystąpienia potencjalnego błędu
try:

    # Tworzymy obiekt gniazda, który posłuży do komunikacji z serwerem
    # Korzystając z konstrukcji with, nie przejmujemy się zamknięciem gniazda,
    # konstrukcja with zrobi to za nas.
    # funkcja socket przyjmuje argumenty: rodzina i typ
    # rodzina AF_INET oznacza, że będziemy korzystać z IPv4
    # typ SOCK_STREAM informuje, że zostanie użyty protokół TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # Wiążemy gniazdo z dowolnym adresem (0.0.0.0)
        # i podanym numerem portu
        server_socket.bind(('0.0.0.0', bind_port))

        # Ustawiamy gniazdo w tryb nasłuchiwania
        # i czekamy na połączenie od klienta
        server_socket.listen(5)
        print("[*] Rozpoczęcie pracy serwera proxy")
        print("Ctrl + C aby zatrzymać")

        # Akceptujemy połączenie od klienta.
        # metoda accept zwraca obiekt gniazda klienta
        # i krotkę z jego adresem i numerem portu
        client_socket, client_address = server_socket.accept()

        # Wypisujemy informację o otrzymanym połączeniu od klienta
        print(f"[+] Odebrano połączenie od [{client_address[0]}:{client_address[1]}]")

        # Tworzymy nowy obiekt gniazda dla połączenia ze zdalnym hostem
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_connection:

            # Łączymy się z zdalnym hostem na podstawie argumentów,
            # z którymi został uruchomiony skrypt
            remote_connection.connect((remote_host, remote_port))

            # Wypisujemy informację o połączeniu ze zdalnym hostem
            print(f"[+] Połączono z [{remote_host}:{remote_port}]")

            # Mapujemy obiekty gniazda:
            # kluczem jest gniazdo, od którego odbieramy dane,
            # a wartością gniazdo, do którego wyślemy odebrane dane.
            sockets = {
                client_socket: remote_connection,
                remote_connection: client_socket
            }

            try:

                # Nieskończona pętla, w której następuje
                # przekazywanie danych między klientem
                # a zdalnym hostem
                while True:

                    # Korzystając z funkcji select, zwracamy listę gniazd,
                    # z których można odbierać dane
                    readable_sockets, _, _ = select.select(sockets.keys(), [], [])

                    # Dla każdego gniazda z listy gniazd
                    # zdatnych do odczytu odbieramy dane
                    for sock in readable_sockets:

                        # Odbieramy dane od gniazda
                        data = sock.recv(2048)

                        # Jeśli nie ma żadnych danych,
                        # wypisujemy informację o przerwanym
                        # połączeniu i skrypt kończy działanie
                        if not data:
                            print("[-] Połączenie przerwane")
                            client_socket.close()
                            print("Kończenie")
                            quit()

                        # Wypisujemy informację o odebraniu danych
                        print("[==>] Odebrano dane")

                        # Wypisujemy na ekran zrzut szesnastkowy
                        # odebranych danych
                        print("[x] Zrzut szesnastkowy:")
                        print(hexdump(data))

                        # Przekazujemy dane do hosta docelowego
                        # korzystając z wcześniej przygotowanej
                        # mapy (słownika)
                        sockets[sock].send(data)

                        # Wypisujemy informację o wysłaniu danych
                        print("[<==] Wysłano dane")

            except KeyboardInterrupt:

                # Po naciśnięciu Ctr + C
                # skrypt kończy działanie
                print("Kończenie")
                client_socket.close()
                quit()

except socket.error as err:

    # Jeśli wystąpił błąd związany z połączeniem sieciowym
    # wypisujemy na ekran komunikat o błędzie
    # i skrypt kończy działanie
    print(err)


'''

Przykład działania:

> python .\proxy_tcp.py 8080 localhost 1337
[*] Rozpoczęcie pracy serwera proxy
[+] Odebrano połączenie od [127.0.0.1:1576]
[+] Połączono z [localhost:1337]
[==>] Odebrano dane
[x] Zrzut szesnastkowy:
61 6c 61 20 6d 61 20 6b 6f 74 61 0a              ala ma kota.
[<==] Wysłano dane
[==>] Odebrano dane
[x] Zrzut szesnastkowy:
66 20 6a 6e 6f 71 77 74 68 33 38 74 20 32 68 74  f jnoqwth38t 2ht
73 6f 34 74 68 34 6f 74 68 33 36 68 74 33 34 36  so4th4oth36ht346
33 34 35 20 68 6b 33 34 79 33 34 36 33 34 2b 2d  345 hk34y34634+-
2f 2f 36 20 2d 33 36 2f 35 33 34 2d 2a 36 0a     //6 -36/534-*6.
[<==] Wysłano dane
[==>] Odebrano dane
[x] Zrzut szesnastkowy:
20 73 61 75 68 77 65 20 34 36 37 38 39 35 33 39   sauhwe 46789539
34 23 24 5e 20 23 24 23 24 32 33 39 35 34 33 20  4#$^ #$#$239543
20 33 34 34 36 39 33 34 30 36 39 33 34 20 0a      344693406934 .
[<==] Wysłano dane
[-] Połączenie przerwane
Kończenie

'''