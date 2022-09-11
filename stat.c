#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <pwd.h>
#include <grp.h>
#include <time.h>

/*

Program realizuje zadanie podobne do
linuksowego polecenia ls -l <plik>

*/

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("usage: %s <filename>\n", argv[0]);
        exit(EXIT_SUCCESS);
    }

    struct stat statbuf;
    char *pathname = argv[1];

    if (stat(pathname, &statbuf) < 0)
    {
        perror("stat");
        exit(EXIT_FAILURE);
    }

     /* sprawdzenie jakiego typu jest plik 
     (za pomoca masek bitowych zdefiniowanych w pliku naglowkowym <sys/stat.h>) */
    switch(statbuf.st_mode & S_IFMT) {
        case S_IFREG:   printf("-");    break; /* zwykly plik */
        case S_IFDIR:   printf("d");    break; /* katalog */
        case S_IFLNK:   printf("l");    break; /* dowiazanie symboliczne */
        case S_IFSOCK:  printf("s");    break; /* gniazdo */
        case S_IFCHR:   printf("c");    break; /* specjalny, znakowy */
        case S_IFBLK:   printf("b");    break; /* specjalny, blokowy */
        case S_IFIFO:   printf("p");    break; /* potok nazwany (fifo) */
        default:        printf("?");    break; /* nieznany typ pliku */
    }

    /* wypisanie praw dostepu do pliku */

    /* prawo do czytania/przeszukiwania przez uzytkownika */
    printf("%c", (statbuf.st_mode & S_IRUSR) ? 'r' : '-');

    /* prawo do modyfikacji/zmiany zawartosci przez uzytkownika */
    printf("%c", (statbuf.st_mode & S_IWUSR) ? 'w' : '-');

    /* prawo do uruchomienia/wejscia przez uzytkownika */
    printf("%c", (statbuf.st_mode & S_IXUSR) ? 'x' : '-');

    /* prawo do czytania/przeszukiwania przez grupe */
    printf("%c", (statbuf.st_mode & S_IRGRP) ? 'r' : '-');

    /* prawo do modyfikacji/zmiany zawartosci przez grupe */
    printf("%c", (statbuf.st_mode & S_IWGRP) ? 'w' : '-');

    /* prawo do uruchomienia/wejscia przez grupe */
    printf("%c", (statbuf.st_mode & S_IXGRP) ? 'x' : '-');

    /* prawo do czytania/przeszukiwania przez innych */
    printf("%c", (statbuf.st_mode & S_IROTH) ? 'r' : '-');

    /* prawo do modyfikacji/zmiany zawartosci przez innych */
    printf("%c", (statbuf.st_mode & S_IWOTH) ? 'w' : '-');

    /* prawo do uruchomienia/wejscia przez innych */
    printf("%c", (statbuf.st_mode & S_IXOTH) ? 'x' : '-');

    /* wypisanie nazwy użytkownika właściciela pliku */
    printf(" %s", getpwuid(statbuf.st_uid)->pw_name);

    /* wypisanie nazwy grupy włąściciela pliku */
    printf(" %s", getgrgid(statbuf.st_gid)->gr_name);

    /* wypisanie rozmiaru pliku */
    printf(" %luB", statbuf.st_size);

    /* data i czas ostatniej modyfikacji pliku */
    char date[50];
    strftime(date, 50, "%Y-%m-%d %H:%M", localtime(&statbuf.st_mtime));
    printf(" %s", date);

    printf("\n");

    return 0;
}