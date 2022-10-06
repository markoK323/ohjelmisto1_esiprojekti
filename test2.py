import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='moimarko',
    autocommit=True
    )


def haeLentokenttanimi():
    tuple = {}
    sql = '''SELECT airport.name as airport_name,country.name as country_name,country.continent from airport,country
    WHERE airport.iso_country = country.iso_country and airport.type = "large_airport" order by rand()'''
    kursori = yhteys.cursor()
    kursori.execute(sql,tuple)
    desc = kursori.description
    column_names = [col[0] for col in desc]
    tulos =[dict(zip(column_names,row))
        for row in kursori.fetchall()]
    return tulos;

testt = []
testt.append(haeLentokenttanimi())
omg = haeLentokenttanimi()
# print(omg[1])
print(testt)