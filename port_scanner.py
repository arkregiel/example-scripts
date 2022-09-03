# port_scanner.py - szukanie otwartych portów TCP na komputerze

import socket   # ta biblioteka jest potrzebna do przeprowadzania operacji sieciowych

addr = input("Podaj prawidłowy adres IPv4: ")
print("Podaj pierwszy i ostatni port skanowanego zakresu (odzielone spacją): ", end='')
port_min, port_max = input().split()

# konwersja numerów portów z str
port_min = int(port_min)
port_max = int(port_max)

# sprawdzimy porty od port_min do port_max
for port in range(port_min, port_max + 1):

    # wykorzystanie bloku try-except oznaczaz
    # że spodziewamy się wystąpienia potencjalnego błędu
    try:
        # funkcja socket przyjmuje argumenty: rodzina i typ
        # rodzina AF_INET oznacza, że będziemy korzystać z IPv4
        # typ SOCK_STREAM informuje, że zostanie użyty protokół TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # czas oczekiwania na połączenie ustawiamy na pół sekundy
            sock.settimeout(0.5) 

            sock.connect((addr, port)) # próba połączenia z portem

            # jeśli nie wystąpił błąd, połączenie się powiodło
            # oznacza to, że port jest otwarty
            print(str(port) + " jest otwarty")
    except:
        # jeśli port jest zamknięty, nie da się z nim połączyć
        # w tej sytuacji zostaje zgłoszony błąd, który ignorujemy
        pass