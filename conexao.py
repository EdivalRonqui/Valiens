import pyodbc
import sqlite3
import json

# Carregar o JSON do arquivo
with open('.\\config.json', 'r') as file:
    config = json.load(file)

# Construir a string de conexão
sibase_config = (
    f"DRIVER={{{config['DRIVER']}}};"
    f"SERVER={config['SERVER']};"
    f"PORT={config['PORT']};"
    f"DATABASE={config['DATABASE']};"
    f"UID={config['UID']};"
    f"PWD={config['PWD']};"
)

# sibase_config = (
#     "DRIVER={ODBC Driver for Sybase};"
#     "SERVER=localhost;"
#     "PORT=2638;"
#     "DATABASE=contabil;"
#     "UID=TI;"
#     "PWD=123456Mudar;"
# )

sqlite_db = '.\\DrContabil.db'

class DatabaseConnections:
    def __init__(self, sibase_config, sqlite_db):
        self.sibase_config = sibase_config
        self.sqlite_db = sqlite_db
        self.sibase_conn = None
        self.sqlite_conn = None

    def connect_sibase(self):
        try:
            self.sibase_conn = pyodbc.connect(self.sibase_config)
            return self.sibase_conn.cursor()
        except pyodbc.Error as e:
            print("Erro ao conectar ao Sibase:", e)
            raise

    def connect_sqlite(self):
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_db)
            return self.sqlite_conn.cursor()
        except sqlite3.Error as e:
            print("Erro ao conectar ao SQLite:", e)
            raise

    def close_connections(self):
        if self.sibase_conn:
            self.sibase_conn.close()
        if self.sqlite_conn:
            self.sqlite_conn.close()

class DataManager:
    def __init__(self, sibase_cursor, sqlite_cursor):
        self.sibase_cursor = sibase_cursor
        self.sqlite_cursor = sqlite_cursor

    def fetch_sibase_data(self, query):
        self.sibase_cursor.execute(query)
        return self.sibase_cursor.fetchall()

    def upsert_data(self, rows, query):
        count = 0
        for row in rows:
            self.sqlite_cursor.execute(query, row)
            count += 1
        print('Linhas inseridas: ', count)
        self.sqlite_cursor.connection.commit()

    def create_table(self, query):
        self.sqlite_cursor.execute(query)
