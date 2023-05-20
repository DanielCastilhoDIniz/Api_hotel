import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()


criar_tabela = "\
        CREATE TABLE IF NOT EXISTS hoteis (\
            hotel_id TEXT PRIMARY KEY,\
            nome TEXT,\
            estrelas REAL,\
            diarias REAL,\
            cidade TEXT\
        )"

criar_hotel = "INSERT INTO hoteis VALUES('Alpha','Alpha Hotel', 4.3, 500.50, 'Recife')"

cursor.execute(criar_tabela)
cursor.execute(criar_hotel)


connection.commit()
connection.close()
