# web_dir_enum.py
# prosty skrypt sprawdzający,
# jakie foldery lub pliki są dostępne
# na serwerze WWW
# (Web Directory Enumeration)

#################################################################
# DISCLAIMER:                                                   #
# Skrypt może potencjalnie posłużyć do pozyskania               #
# wrażliwych informacji na temat aplikacji webowej lub          #
# może naruszać regulamin użytkowania tej aplikacji.            #
# Ten skrypt służy przede wszystkim celom edukacyjnym           #
# i należy go uruchamiać TYLKO w ramach testowania              #
# bezpieczeństwa własnego systemu lub systemu, na którego       #
# testowanie bezpieczeństwa mamy wyraźną zgodę i działamy       #
# wyłącznie w celu poprawy jego bezpieczeństwa                  #
# (artykuły 267 oraz 269b Kodeksu karnego).                     #
# NIE POPIERAM i NIE ZACHĘCAM do ŻADNYCH nielegalnych działań.  #
#################################################################

# Moduł requests pozwala na
# tworzenie żądań HTTP do serwera WWW
# https://requests.readthedocs.io/en/latest/
# Można go zainstalować poleceniem:
# pip install requests
import requests

# Krotka zawierająca typowe foldery i pliki,
# które można znaleźć na serwerze WWW.
# Zazwyczaj testerzy bezpieczeństwa korzystają
# z plików txt zawierających tysiące takich ścieżek
common_paths = (
    'admin',
    'administrator',
    'img',
    'images',
    'logs',
    'test',
    'cgi-bin',
    'tmp',
    'templates',
    'plugins',
    'cache',
    'robots.txt',
)

# prosimy użytkownika od adres URL strony,
# której foldery zamierza przejrzeć
website = input("Podaj adres URL strony: ")

# adres URL powinien zaczynać się od protokołu (HTTP lub HTTPS)
if not website.startswith('http://') and not website.startswith('https://'):
    print('Adres strony powinien zaczynać się od http:// lub https://')
    quit()

# na końcu adresu podanego URL
# powinien znajdować się znak /
if not website.endswith('/'):
    website += '/'

# przejście po wszystkich ścieżkach,
# które zamierzamy sprawdzić
for path in common_paths:

    # łączymy adres URL strony 
    # z sprawdzaną ścieżką
    url = website + path

    # wykonujemy żądanie GET do strony
    response = requests.get(url)

    # Jeśli kod HTTP to 200 (OK),
    # znaczy, że folder/plik znajduje się
    # na serwerze i mamy do niego dostęp
    if response.status_code == 200:
        print(url)
