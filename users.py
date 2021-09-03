import psycopg2

from psycopg2 import connect

import argparse

from models import User, check_password, hash_password

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
connection = connect(user=USER, password=PASSWORD, host=HOST, dbname='warsztat_1_db')
connection.autocommit = True
cursor = connection.cursor()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()


username = args.username
password = args.password
new_pass = args.new_pass


def add_user(username, password):
    if len(password) >= 8:
        try:
            temp = User(username, password)
            temp.save_to_db(cursor)
        except psycopg2.errors.UniqueViolation:
            print("Taki użytkownik już istnieje!")
            return None
    else:
        print("Za krótkie hasło!")
        return None

def edit_user(username, password, new_pass):
    sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
    cursor.execute(sql, (username,))
    data = cursor.fetchone()
    if check_password(password, data[2]) is True:
        if len(password) >= 8:
            hashed_password = hash_password(new_pass)
            sql = "UPDATE users SET hashed_password=%s WHERE username=%s;"
            cursor.execute(sql, (hashed_password, username))
        else:
            return "Nowe hasło jest za krótkie!"
    else:
        return "Podałeś niepoprawne hasło!"


def delete_user(username, password):
    sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
    cursor.execute(sql, (username,))
    data = cursor.fetchone()
    if check_password(password, data[2]) is True:
        sql = "DELETE FROM users WHERE username=%s;"
        cursor.execute(sql, (username))
        return f"Użytkownik {username} został usunięty!"
    else:
        return "Podałeś niepoprawne hasło!"


def user_list():
    sql = "SELECT id, username FROM users;"
    cursor.execute(sql, (username,))
    result = []
    for row in cursor:
        result.append(row)
        print("Lista użytkowników: ")
        print(row)
    return result


if args.username and args.password and args.edit and args.new_pass:
    edit_user(args.username, args.password, args.new_pass)
elif args.username and args.password and args.delete:
    delete_user(args.username, args.password)
elif args.username and args.password:
    add_user(args.username, args.password)
elif args.list:
    user_list()
else:
    parser.print_help()

cursor.close()
connection.close()










