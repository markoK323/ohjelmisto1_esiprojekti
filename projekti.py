import mysql.connector
import itertools
import random

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='moimarko',
         autocommit=True
         )


# funktio jolla haetaan lentokentän nimi, maa ja maanosa.
def haeLentokenttanimi():
    sql = '''SELECT airport.name as airport_name,country.name as country_name,country.continent from airport,country
    WHERE airport.iso_country = country.iso_country and airport.type = "large_airport" order by rand() limit 1'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    tulos_lista = list(itertools.chain(*tulos))
    return tulos_lista;


# funktio jolla haetaan vanha highscore ja nimi
def getScoreName():
    sql = "SELECT nimi, highscore FROM user WHERE highscore = ( SELECT MAX(highscore) FROM user )"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    nimilista = list(itertools.chain(*tulos))
    return nimilista;


# funktio joka kerää vihjeeseen maita listaan.
def Vihjelista(continent, country):
    tuple = (continent, country,)
    sql = '''Select country.name from country where continent = %s and country.name not in(%s) order by rand() limit 4'''
    kursori = yhteys.cursor()
    kursori.execute(sql, tuple)
    tulos = kursori.fetchall()
    tulos_lista = list(itertools.chain(*tulos))
    tulos_lista.append(country)
    random.shuffle(tulos_lista)
    return tulos_lista;

#funktio jolla saadaan score
def getScore():
    sql="SELECT MAX(highscore) FROM user"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    scorelista = list(itertools.chain(*tulos))
    return scorelista;

# funktio jolla kirjoitetaan nickname ja highscore tietokantaan
def kirjoitaTietokantaan():
    kursori = yhteys.cursor()
    tuple = (nickName, currentScore)
    sql = "INSERT INTO user (nimi, highscore) VALUES(%s, %s)"
    kursori.execute(sql, tuple)
    print(kursori.rowcount, "record inserted.")
    return;


# funktio jolla luodaan table user jos sitä ei ole olemassa.
def createTableUser():
    kursori = yhteys.cursor()
    sql = "CREATE TABLE IF NOT EXISTS user (nimi varchar(10), highscore int);"
    kursori.execute(sql)
    return;


# arvotaan lentokenttä
omg = haeLentokenttanimi()

# luodaan table user if not exist
createTableUser()

vanhaHighScore = getScore()

# kertoimet, healthit, pisteet
kerroin = 1
health = 3
currentScore = 0

# pelin alkuteksti
print("Guess countries by their airports. You have 3 healths. For correct answers you get points.")
print("On the first guess you can get 100 points, on the second guess 75 and on the third 50.")
print("For 3 wrong guesses a row you will lose 1 health.")

# nickname mahdollista highscorea varten
nickName = input("Enter nickname: ")

while health > 0:
    kysymys = str(input(f"In which country is {omg[0]} located?: "))

    # Arvaus oikein:
    if kysymys == omg[1]:
        print("Correct answer!")
        # haetaan uusi lentokenttä:
        omg = haeLentokenttanimi()
        # lisätään scorea:
        currentScore = currentScore + kerroin * 100
        print(f"You get {kerroin * 100} points")
        # pistekerrointa nostetaan:
        kerroin = kerroin + 1

    # vastaus väärin:
    else:
        print("Wrong answer.")
        # syötetään vihjeenä maanosa
        print(f"Hint: continent: {omg[2]}")
        # kerroin nollataan
        kerroin = 1
        kysymys = str(input("Guess again: "))

        if kysymys == omg[1]:
            print("Correct answer!")
            print("You get 75 points!")
            omg = haeLentokenttanimi()
            currentScore = currentScore + 75
        else:
            print("Wrong answer.")
            Hints = Vihjelista(omg[2], omg[1])
            print(
                f"Hint: It is in one of the following countries: {Hints[0]}, {Hints[1]}, {Hints[2]}, {Hints[3]}, {Hints[4]}")
            kysymys = str(input("Guess again: "))

            if kysymys == omg[1]:
                print("Correct answer!")
                print("You get 50 points!")
                omg = haeLentokenttanimi()
                currentScore = currentScore + 50
            else:
                print("Wrong answer.")
                print(f"Correct answer is {omg[1]}")
                print("You lose 1 health")
                omg = haeLentokenttanimi()
                health = health - 1
                print('Healths left: ', health, 'Your score: ', currentScore)

# jos currentscore on suurempi kuin vanha score  tai vanha highscore on tyhjä lisätään se tietokantaan nicknamen kanssa
if vanhaHighScore[0] == None:
    kirjoitaTietokantaan()
elif vanhaHighScore[0] < currentScore:
    kirjoitaTietokantaan()

# tulostetaan omat pisteet ja vanhat highscore ja name
print(f"Your score: {currentScore}")
print(f"Highscore: {getScoreName()[0]} with score {getScoreName()[1]}")