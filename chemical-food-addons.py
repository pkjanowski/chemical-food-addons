import requests
from bs4 import BeautifulSoup

response = requests.get(
    'https://pl.wikipedia.org/wiki/Lista_chemicznych_dodatk%C3%B3w_do_%C5%BCywno%C5%9Bci#E100%E2%80%93E199_(barwniki)')

soup = BeautifulSoup(response.text, 'html.parser')
e_code = []
e_name = []
rows = []

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
            if (user_e_name in e):
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

for row in rows:
    for set in row:
        if set.find('td') != None:
            e_code.append(set.find_all('td')[0].text)
            e_name.append(set.find_all('td')[1].text)


# konwersja wszystkich elementów listy na małe litery
e_name = [element.lower() for element in e_name];
e_name

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