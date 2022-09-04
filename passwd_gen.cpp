/*

passwd_gen.cpp

Generowanie losowego hasła o podanej długości

*/

#include <iostream>     // cin, cout
#include <stdlib.h>     // srand, rand
#include <time.h>       // time
#include <string>       // string

// korzystamy z konkretnych rzeczy
// z przestrzeni nazw std
using std::cout;
using std::cin;
using std::endl;
using std::string;

int main()
{
    // inicjalizacja generatora liczb pseudolosowych
    srand(time(NULL));

    string password = "";   // zmienna przechowująca wygenerowane hasło

    cout << "Podaj dlugosc hasla: ";
    int passwordLength; // zmienna przechowująca długość generowanego hasła
    cin >> passwordLength;  // użytkownik podaje, jaką długość ma mieć hasło

    // generujemy passwordLength znaków
    for (int i = 0; i < passwordLength; ++i)
    {
        // losujemy liczbę z przedziału od 33 (!) do 126 (~),
        // która jest kodem ASCII znaku, a następnie zapamiętujemy
        // znak odpowiadający tej liczbie w tabeli ASCII
        // https://www.rapidtables.com/code/text/ascii-table.html
        char character = (char)(rand() % ('~' - '!' + 1) + '!');

        // dodajemy znak do hasła
        password += character;
    }

    // wypisujemy wygenerowane hasło
    cout << "Twoje wygenerowane haslo: " << password << endl;

    return 0;
}