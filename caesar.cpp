#include <iostream>
#include <string>

using namespace std;

enum CaesarCipherOperation { encrypt, decrypt};

string caesarCipher(int key, string plaintext, CaesarCipherOperation oper)
{
    string ciphertext = "";

    for (int i = 0; i < plaintext.length(); ++i)
    {
        char character = plaintext[i];
        char characterEncrypted;
        if (oper == encrypt)
        {
            characterEncrypted = (character - ' ' + key) % ('~' - ' ' + 1) + ' ';
        }
        else if (oper == decrypt)
        {
            characterEncrypted = (character - ' ' - key);
            if (characterEncrypted < 0)
                characterEncrypted = 95 + characterEncrypted;
            characterEncrypted = (characterEncrypted % ('~' - ' ' + 1)) + ' ';
        }
        ciphertext += characterEncrypted;
    }

    return ciphertext;
}

int main()
{
    cout << "Podaj dane: ";
    string data;
    getline(cin, data);
    cout << "Podaj klucz: ";
    int key;
    cin >> key;

    int choice;
    while (true)
    {
        cout << "Co chcesz zrobic?" << endl;
        cout << "1. zaszyfrowac" << endl;
        cout << "2. odszyfrowac" << endl;
        cout << "> ";
        
        cin >> choice;

        if (choice == 1 || choice == 2)
            break;
        
        cout << "Podaj cyfre 1 lub 2" << endl;
    }

    CaesarCipherOperation oper;
    if (choice == 1)
        oper = encrypt;
    else
        oper = decrypt;

    string processedData = caesarCipher(key, data, oper);

    cout << "Twoje przetworzone dane:" << endl;
    cout << processedData << endl;

    return 0;
}
