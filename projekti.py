import mysql.connector
import itertools

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='moimarko',
         autocommit=True
         )

#funktio jolla haetaan lentokentän nimi, maa ja maanosa.
def haeLentokenttanimi():
    sql = '''SELECT airport.name as airport_name,country.name as country_name,country.continent from airport,country
    WHERE airport.iso_country = country.iso_country and airport.type = "large_airport" order by rand() limit 1'''
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    tulos_lista = list(itertools.chain(*tulos))
    return tulos_lista;

#funktio jolla haetaan vanha highscore
def getScore():
    sql="SELECT MAX(highscore) FROM user"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    scorelista = list(itertools.chain(*tulos))
    return scorelista;

#funktio jolla haetaan vanha highscore ja nimi
def getScoreName():
    sql = "SELECT nimi, highscore FROM user WHERE highscore = ( SELECT MAX(highscore) FROM user )"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    nimilista = list(itertools.chain(*tulos))
    return nimilista;

#funktio jolla kirjoitetaan nickname ja highscore tietokantaan
def kirjoitaTietokantaan():
    kursori = yhteys.cursor()
    tuple = (nickName, currentScore)
    sql = "INSERT INTO user (nimi, highscore) VALUES(%s, %s)"
    kursori.execute(sql, tuple)
    # print(kursori.rowcount, "record inserted.")
    return;

omg = haeLentokenttanimi()

kerroin = 1
health = 3
currentScore = 0

print('GUESS COUNTRIES BY THEIR AIRPORTS. U HAVE 3 HEALTH. FOR CORRECT ANSWERS U GET POINTS.'
      '\nON THE FIRST GUESS U CAN GET 100 POINTS, ON THE SECOND GUESS 75 AND ON THE THIRD 50.' 
      '\nFOR 3 WRONG GUESSES IN A ROW U WILL LOSE 1 HEALTH.')

#lista jossa on haettu tietokannasta highscore
vanhaHighScore = getScore()
nickName = input("Enter nickname: ")

while health > 0:
    kysymys_ask = str(input(f"In which country is {omg[0]} located?: "))
    kysymys = kysymys_ask.capitalize()
    if kysymys == omg[1]:
        print("Correct answer!")
        omg = haeLentokenttanimi()
        currentScore = currentScore + kerroin*1
        kerroin = kerroin +1
    else:
        print("Wrong answer.")
        print(f"Continent: {omg[2]}")
        kerroin=1
        kysymys = str(input("Guess again: "))
        if kysymys == omg[1]:
            print("Correct answer!")
            omg = haeLentokenttanimi()
            currentScore = currentScore+0.5
        else:
            print("Wrong answer.")
            omg = haeLentokenttanimi()
            health = health-1
    print('Healths left: ',health, 'Your score: ',currentScore)

#jos currentscore on suurempi kuin vanha score  tai vanha highscore on tyhjä lisätään se tietokantaan nicknamen kanssa
if vanhaHighScore[0] == None:
    kirjoitaTietokantaan()
elif vanhaHighScore[0] < currentScore:
    kirjoitaTietokantaan()

#tulostetaan omat pisteet ja vanhat highscore ja name
print(f"Highscore: {getScoreName()[0]} with score {getScoreName()[1]}")