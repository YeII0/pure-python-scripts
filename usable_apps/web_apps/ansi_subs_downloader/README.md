Program do pobierania napisów z ansi.


Wymagane składniki niezbędne dla uruchomienia programu:
1. Python 3.7.4 lub nowszy.
2. 5 zewnętrznych bibliotek:
    - requests,
    - beautifulsoup4,
    - aiohttp,
    - cchardet,
    - aiodns.

Biblioteki można zainstalować po uprzednim zainstalowaniu pythona. 
Aby to zrobić należy wejść do wiersza poleceń i wykonać:
    - "pip install requests"
    - "pip install --upgrade requests"
    - "pip install beautifulsoup4"
    - "pip install --upgrade beautifulsoup4"
    - "pip install aiohttp[speedups]"
Ostatnia linijka instaluję trzy ostatnie biblioteki wymienione w punkcie drugim.
Linijki z "--upgrade" aktualizuję biblioteki do najnowszej wersji.


Sposób użycia programu:
1. W pierwszym kroku należy podać miejsce do pobrania napisów.
2. W drugim kroku należy podać od 1 do 3 argumentów oddzielonych średnikiem bez żadnych spacji:
    - 1 argument - strona wyszukiwarki z napisami do pobrania,
    - 2 argument (opcjonalny) - mogą nim być:
        - liczba oznaczająca ostatnią stronę do której będzie kontynuowane pobieranie napisów,
        - słowo kluczowe "norename" oznaczające, że w nazwach napisów nie będą zamieniane kojelność autora i epizodu.
    - 3 argument (opcjonalny) - używany tylko wtedy gdy w drugim argumencie podana jest liczba.
      Argumentem jest słowo kluczowe "norename" oznaczające, że w nazwach napisów nie będą zamieniane kojelność autora i epizodu.
3. Powrót do kroku 2. Gdy zostaną pobrane napisy, można ponownie pobrać inne stosując się do kroku drugiego. 
   Z programu można wyjść jakkolwiek, na przykład krzyżykiem. Program nie przechowuję żadnych danych więc się nie zepsuję.


Przykłady dla 2 kroku:
Przykład 1:
    http://animesub.info/szukaj.php?szukane=Sword+Art+Online&pTitle
    Podano jeden argument. Zostaną pobrane napisy tylko z wyszukiwarki podanej w argumencie.

Przykład 2:
    http://animesub.info/szukaj.php?szukane=Sword+Art+Online&pTitle;norename
    Podano dwa argumenty. Drugi argument "norename" oznacza, że nazwy plików nie będą zmieniane. 
    Domyślnie bez podania argumentu "norename" w nazwach plików zamieniane są kolejność autora i epizodu.

Przykład 3:
    http://animesub.info/szukaj.php?szukane=Sword+Art+Online&pTitle;4
    Podano dwa argumenty z czego drugi jest liczbą. W tym wypadku 2 argument oznacza stronę do której chcemy kontynuować pobieranie napisów.
    Liczba musi być większa niż strona na którą wskazuję pierwszy argument. W tym wypadku w pierwszym argumencie podany jest adres do wyszukiwarki
    wskazującej na pierwszą stronę wyszukiwania. W przykładzie pobierane będą napisy od 1 do 4 strony. 
    Pierwszy argument nie musi wskazywać na pierwszą stronę.

Przyklad 4:
    http://animesub.info/szukaj.php?szukane=Sword+Art+Online&pTitle;4;norename
    Podano 3 argumenty. Działanie prawie jak w poprzednim przykładzie. 
    Jedyną różnicą jest to, że w nazwach plików nie będzie zamieniana kolejność autora i epizodu, na co wskazuję 3 argument "norename".


Autor: Zimbzon książe Afryki.
Kontakt: discord -> Yello#8637.