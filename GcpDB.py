#GcpDb.py
#Simple Wrapper for Google Cloud SQL API

import os
import pymysql
from flask import jsonify
import re

db_user = os.environ.get("CLOUD_SQL_USERNAME")
db_pass = os.environ.get("CLOUD_SQL_PASSWORD")
db_name = os.environ.get("CLOUD_SQL_DATABASE_NAME")
db_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

def open_connection():
    unix_socket = "/cloudsql/" + db_connection_name
    try:
        if os.environ.get("GAE_ENV") == "standard":
            conn = pymysql.connect(user=db_user, password=db_pass,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        return jsonify({"error": str(e)})
    return conn

#SQL Table Structure
# Tables:
#   - Users
#       - UserName
#       - Email
#       - Password (Hashed)
#       - UserID
#   - Chat_1
#       - Messages:
#           - MessageID
#           - content
#           - sender (UserID)
#           - timestamp
#           - response_to (MessageID)
#   - Chat_2
#       - Messages:
#           - MessageID
#           - content
#           - sender (UserID)
#           - timestamp
#           - response_to (MessageID)
#   - Chat_n


# Chat Functions
def chat_exists(chat_id: int) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE %s", (table_name,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

def create_chat(chat_id: int) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("CREATE TABLE %s (MessageID INT AUTO_INCREMENT PRIMARY KEY, content VARCHAR(255), sender INT, timestamp INT, response_to INT)", (table_name,))
        conn.commit()
        return True

def get_chat(chat_id: int) -> list:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM %s", (table_name,))
        result = cursor.fetchall()
        return result

def delete_chat(chat_id: int) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE %s", (table_name,))
        conn.commit()
        return True

# Message Functions
def add_message(chat_id: int, content: str, sender: int, timestamp: int, response_to: int) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO %s (content, sender, timestamp, response_to) VALUES (%s, %s, %s, %s)", (table_name, content, sender, timestamp, response_to))
        conn.commit()
        return True

def patch_message(chat_id: int, message_id: int, content: str) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("UPDATE %s SET content=%s WHERE MessageID=%s", (table_name, content, message_id))
        conn.commit()
        return True

def delete_message(chat_id: int, message_id: int) -> bool:
    conn = open_connection()
    table_name = "Chat_" + str(chat_id)
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM %s WHERE MessageID=%s", (table_name, message_id))
        conn.commit()
        return True


# User Functions
def confirm_login(user_identifier, hashed_password) -> bool:
    email = re.search(r'[\w\.-]+@[\w\.-]+', user_identifier)
    conn = open_connection()
    with conn.cursor() as cursor:
        if email:
            cursor.execute("SELECT * FROM Users WHERE Email=%s AND Password=%s", (user_identifier, hashed_password))
        else:
            cursor.execute("SELECT * FROM Users WHERE UserName=%s AND Password=%s", (user_identifier, hashed_password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

def user_exists(username: str) -> bool:
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE UserName=%s", (username,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

def create_user_db(username: str, hashed_password: str, email: str = "") -> bool:
    if user_exists(username):
        return False
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Users (UserName, Password, Email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        conn.commit()
        return True