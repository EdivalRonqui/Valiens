import pyodbc
import sqlite3
from conexao import DatabaseConnections, sibase_config, sqlite_db, DataManager
import queries

def main():
    
    db_connections = DatabaseConnections(sibase_config, sqlite_db)
    try:
        sibase_cursor = db_connections.connect_sibase()
        sqlite_cursor = db_connections.connect_sqlite()

        data_manager = DataManager(sibase_cursor, sqlite_cursor)
        
        qry = {
            "LanCredito": [queries.select_query_LanCredito, queries.upsert_query_LanCredito, queries.create_query_LanCredito],
            "LanDebito": [queries.select_query_LanDebito, queries.upsert_query_LanDebito, queries.create_query_LanDebito],
            "Acumuladores": [queries.select_query_Acumuladores, queries.upsert_query_Acumuladores, queries.create_query_Acumuladores],
            "LanFisImpostosEntradas": [queries.select_query_LanFisImpostosEntradas, queries.upsert_query_LanFisImpostosEntradas, queries.create_query_LanFisImpostosEntradas],
            "LanFisImpostosSaidas": [queries.select_query_LanFisImpostosSaidas, queries.upsert_query_LanFisImpostosSaidas, queries.create_query_LanFisImpostosSaidas],
            "LanFisImpostosServicos": [queries.select_query_LanFisImpostosServicos, queries.upsert_query_LanFisImpostosServicos, queries.create_query_LanFisImpostosServicos],
            "FisAcumuladores": [queries.select_query_FisAcumuladores, queries.upsert_query_FisAcumuladores, queries.create_query_FisAcumuladores],
            "LanFisEntradas": [queries.select_query_LanFisEntradas, queries.upsert_query_LanFisEntradas, queries.create_query_LanFisEntradas],
            "LanFisSaidas": [queries.select_query_LanFisSaidas, queries.upsert_query_LanFisSaidas, queries.create_query_LanFisSaidas],
            "LanFisServicos": [queries.select_query_LanFisServicos, queries.upsert_query_LanFisServicos, queries.create_query_LanFisServicos]
        }

        for table, query in qry.items():
            # data_manager.create_table(query[2])
            print("Inserindo dados na tabela:", table)
            rows = data_manager.fetch_sibase_data(query[0])
            data_manager.upsert_data(rows, query[1])
    
    except pyodbc.Error as e:
        print("Erro ao conectar ou consultar o Sibase:", e)
    except sqlite3.Error as e:
        print("Erro ao conectar ou inserir dados no SQLite:", e)
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
    finally:
        db_connections.close_connections()

if __name__ == "__main__":
    main()



