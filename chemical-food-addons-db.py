import requests
from bs4 import BeautifulSoup
import sqlite3

response = requests.get(
    'https://pl.wikipedia.org/wiki/Lista_chemicznych_dodatk%C3%B3w_do_%C5%BCywno%C5%9Bci#E100%E2%80%93E199_(barwniki)')

soup = BeautifulSoup(response.text, 'html.parser')
e_code = []
e_name = []
rows = []
codes = []

e_database = sqlite3.connect('e_database.db')

cur = e_database.cursor()

cur.execute("DROP TABLE IF EXISTS E_TABLE;")

cur.executescript("""
    CREATE TABLE IF NOT EXISTS E_TABLE
    (ID INTEGER PRIMARY KEY ASC,
    KOD varchar(10) NOT NULL,
    NAZWA varchar(250) NOT NULL)""")
e_database.commit()


# sprawdzenie czy kod e istnieje -> jeśli tak to zwrotka z nazwa
def check_e_code(user_e):
    if any(user_e in e for e in e_code):
        counter = 0
        for e in e_code:
            if user_e in e:
                print(e + " " + e_name[counter])
            counter = counter + 1
    else:
        print("Brak kodu w bazie")


# sprawdzenie czy nazwa e istnieje -> jeśli tak to zwrotka z kodem e
def check_e_name(user_e_name):
    if any(user_e_name in e for e in e_name):
        counter = 0
        for e in e_name:
            if user_e_name in e:
                print(e_code[counter] + " " + e)
            counter = counter + 1
    else:
        print("Brak nazwy w bazie")


# sprawdzenie poprawnosci wejscia
def inputChoice():
    number = input("Twój wybór: ")
    if number.isdigit():
        return int(number)
    else:
        print("Brak takiej opcji w menu, wybierz właściwą opcję!")
        inputChoice()


tables = soup.find_all("table", class_="wikitable sortable")
for table in tables:
    rows.append(table.find_all('tr'))

e_database = sqlite3.connect("e_database.db")

for row in rows:
    for setx in row:
        if setx.find('td') is not None:
            cur.execute("INSERT INTO E_TABLE VALUES (NULL,?,?);", (setx.find_all('td')[0].text, (setx.find_all('td')[1].text).lower()))
            e_database.commit()

cur.execute("SELECT KOD, NAZWA FROM E_TABLE")

codes = cur.fetchall()

e_database.close()

#rozbicie listy list na pojedyncze listy
e_code, e_name = zip(*codes)

print("Ten program jest bazą dodatków chemicznych do żywności.\n"
      "Wybierz opcję \"Podaj e\" aby przeszkać bazę pod kątem numeru e, lub \"Podaj nazwę\" aby przeszukać pod kątem nazwy. \n"
      "Obie opcje przeszukją cząstkowo, tj. po wprowadzeniu \"e12\" program zwróci wszyskie e zaczynające się od \"e12\"")

while True:
    print("\n(1) Podaj e")
    print("(2) Podaj nazwę")
    print("(3) Wyjdź")

    choice = inputChoice()

    if choice == 1:
        user_e = input("Podaj kod e: ").upper()
        check_e_code(user_e)
    elif choice == 2:
        user_e_name = input("Podaj nazwe e: ").lower()
        check_e_name(user_e_name)
    elif choice == 3:
        break;

print("Koniec programu!")
