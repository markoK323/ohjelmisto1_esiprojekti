import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='moimarko',
    autocommit=True
    )

nimi_variable = input('Anna nimesi: ')
highscore_variable = 50
def kirjoitaTietokantaan():
    kursori = yhteys.cursor()
    tuple = (nimi_variable, highscore_variable)
    # sql = "INSERT INTO user (nimi, highscore) VALUES('{}', '{}')".format(nimi_variable, highscore_variable)
    sql = "INSERT INTO user (nimi, highscore) VALUES(%s, %s)"
    kursori.execute(sql, tuple)
    print(kursori.rowcount, "record inserted.")
    return;


# kirjoitaTietokantaan()

## to do: create sql values as variables so nicname and highscore can be asked and added to database