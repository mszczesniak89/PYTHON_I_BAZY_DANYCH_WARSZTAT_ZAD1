import psycopg2
from psycopg2 import connect

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"

def create_db_sql(query: str):
    connection = connect(user=USER, password=PASSWORD, host=HOST)
    connection.autocommit = True

    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except psycopg2.errors.DuplicateDatabase:
        print("Baza już istnieje!")
        return None


    cursor.close()
    connection.close()

    print("Baza danych utworzona!")
    return None


def create_table_users_sql(query: str, database_name: str):
    connection = connect(user=USER, password=PASSWORD, host=HOST, dbname=database_name)
    connection.autocommit = True

    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except psycopg2.errors.DuplicateTable:
        print("Tabela już istnieje!")
        return None


    cursor.close()
    connection.close()

    print("Tabela utworzona!")
    return None




create_db_sql("CREATE DATABASE warsztat_1_db")
create_table_users_sql("CREATE TABLE users (id serial, username varchar(255), hashed_password varchar(80), PRIMARY KEY(id));", 'warsztat_1_db')
create_table_users_sql("CREATE TABLE messages (id serial, from_id int, to_id int, creation_date timestamp, text varchar(255), PRIMARY KEY(id), FOREIGN KEY(from_id) REFERENCES users(id), FOREIGN KEY(to_id) REFERENCES users(id));", 'warsztat_1_db')





