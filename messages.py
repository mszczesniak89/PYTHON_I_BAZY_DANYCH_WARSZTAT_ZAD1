import psycopg2
import argparse
from psycopg2 import connect
from clcrypto import hash_password, check_password, generate_salt
from datetime import datetime
from models import User


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="user receiving your message")
parser.add_argument("-s", "--send", help="your message")
parser.add_argument("-l", "--list", help="list messages", action="store_true")
args = parser.parse_args()

username = args.username
password = args.password
to_user = args.to
text = args.send


USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
connection = connect(user=USER, password=PASSWORD, host=HOST, dbname='warsztat_1_db')
connection.autocommit = True
cursor = connection.cursor()


class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None



    @property
    def id(self):
        return self._id


    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date) VALUES (%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, datetime.now())
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        # else:
        #     sql = """UPDATE messages SET text=%s WHERE id=%s"""
        #     values = (self._id)
        #     cursor.execute(sql, values)
        #     return True



    @staticmethod
    def load_all_messages(cursor, username):
        sql = "SELECT * FROM Messages WHERE username=%s"
        messages = []
        cursor.execute(sql, (username,))
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_message = Message()
            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.creation_date = creation_date
            loaded_message.text = text
            messages.append(loaded_message)
        return messages



# test = Message(2, 5, "Hello mate!")
# test.save_to_db(cursor)

if args.username and args.password and args.to and args.send:
    sql = "SELECT id, username, hashed_password FROM users WHERE username=%s;"
    cursor.execute(sql, (username,))
    data = cursor.fetchone()
    if check_password(password, data[2]) is True:
        temp1 = User.load_user_by_username(cursor, args.username)
        temp2 = User.load_user_by_username(cursor, args.to)
        mess = Message(temp1.id, temp2.id, args.send)
        cursor = connection.cursor()
        mess.save_to_db(cursor)



    else:
        print("Podałeś niepoprawne hasło!")
elif args.username and args.password and args.list:
    sql = "SELECT id, username, hashed_password FROM messages WHERE username=%s;"
    cursor.execute(sql, (args.username,))
    data = cursor.fetchone()
    if check_password(password, data[2]) is True:
        Message.load_all_messages(cursor, args.username)
    else:
        print("Podałeś niepoprawne hasło!")



        cursor.close()
        connection.close()













