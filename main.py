from flask import Flask, jsonify, render_template, request
from dataclasses import dataclass
import os
import time
import csv
import sqlite3
import requests
import hashlib

app = Flask(__name__)
connection = sqlite3.connect("data/database.db")
cursor = connection.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        last_online INTEGER,
        chat_ids TEXT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS chats (
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_name TEXT,
        chat_password TEXT,
        users TEXT,
        admins TEXT
        )""")

connection.commit()


class Encrypted_text:
    def __init__(self) -> None:
        self.text = ""
    
    def encrypt(self, text, key):
        self.text = ""
        for i in range(len(text)):
            self.text += chr(ord(text[i]) + key)
        return self.text
    
    def decrypt(self, text, key):
        output = ""
        for char in text:
            output += chr(ord(char) - key)
        return output

    def __str__(self) -> str:
        return self.text


class User:
        
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.last_online = int(time.time())
        self.chat_ids = []

        cursor.execute("INSERT INTO users (username, password, last_online, chat_ids) VALUES (:username, :password, :last_online, :chat_ids)", {"username": self.username, "password": self.password, "last_online": self.last_online, "chat_ids": str(self.chat_ids)})
        connection.commit()
        
    
    def __str__(self) -> str:
        return self.username
    
    def to_json(self):
        j = {
            "username": self.username,
            "user_id": self.user_id,
            "password": self.password,
            "last_online": self.last_online,
            "chat_ids": self.chat_ids
        }
        return j
    
    def add_chat(self, chat):
        self.chat_ids.append(chat)
    
    def update_last_online(self):
        self.last_online = int(time.time())

class Chat:
    def __init__(self):
        self.chat_name: str = ""
        self.chat_password: str = ""
        self.users = []
        self.admins = []
        self.messages = []
        self.chat_id = 0
    
    def create(self, chat_name, chat_password):
        self.chat_name = chat_name
        self.chat_password = chat_password
        
        cursor.execute("INSERT INTO chats (chat_name, chat_password, users, admins) VALUES (:chat_name, :chat_password, :users, :admins)", {"chat_id": self.chat_id, "chat_name": self.chat_name, "chat_password": self.chat_password, "users": str(self.users), "admins": str(self.admins)})
        connection.commit()

        self.chat_id = cursor.execute("SELECT chat_id FROM chats WHERE chat_id = (SELECT MAX(chat_id) FROM chats)").fetchone()[0]

        sql_cmd = "CREATE TABLE IF NOT EXISTS messages" + str(self.chat_id) + " (message_id INTEGER PRIMARY KEY AUTOINCREMENT, sender INTEGER, content TEXT, timestamp INTEGER, response_to INTEGER)"
        cursor.execute(sql_cmd)
        
        connection.commit()

        return self        
    
    def append_message(self, message):
        sql_cmd = "INSERT INTO messages" + str(self.chat_id) + " (sender, content, timestamp, response_to) VALUES (:sender, :content, :timestamp, :response_to)"
        cursor.execute(sql_cmd, {"sender": message.sender, "content": message.content, "timestamp": message.timestamp, "response_to": message.response_to})
        connection.commit()
    
    def append_user(self, user):
        user_id = user.user_id
        self.users.append(user_id)
        cursor.execute("UPDATE chats SET users = :users WHERE chat_id = :chat_id", {"users": str(self.users), "chat_id": self.chat_id})
        connection.commit()

    def __str__(self) -> str:
        return self.chat_name
    
    def to_json(self):
        messages = [m.to_json() for m in self.messages]
        users = [u.to_json() for u in self.users]
        j = {
            "chat_id": self.chat_id,
            "chat_name": self.chat_name,
            "chat_password": self.chat_password,
            "messages": messages,
            "users": users,
            "admins": self.admins
        }
        return j

class Message:
    def __init__(self, chat_id, sender, content, response_to = None):
        self.chat_id = chat_id
        self.sender = sender
        self.content = content
        self.timestamp = int(time.time())
        self.response_to = response_to
    
    
    def __str__(self) -> str:
        return self.content
    
    def to_json(self):
        j = {
            "message_id": self.message_id,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp,
            "response_to": self.response_to
        }
        return j

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/get_chat/<chat_id>")
def get_chat(chat_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    sql_cmd = "SELECT * FROM chats WHERE chat_id = messages" + str(chat_id)
    cursor.execute(sql_cmd)
    messages = cursor.fetchall()
    if len(messages) == 0:
        return jsonify({"error": "Chat not found"})
    else:
        return jsonify(messages)

@app.route("/api/create_chat/<chat_name>/<chat_password>")
def create_chat(chat_name, chat_password):
    chat = Chat().create(chat_name, chat_password)
    return jsonify(chat.to_json())
 
create_chat("test", "test")

@app.route("/api/send_message", methods=["POST"])
def send_message():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    data = request.get_json()
    chat_id = data["chat_id"]
    sender = data["sender"]
    content = data["content"]
    response_to = data["response_to"] if "response_to" in data else None
    
    sql_cmd = "INSERT INTO messages" + str(chat_id) + " (sender, content, timestamp, response_to) VALUES (:sender, :content, :timestamp, :response_to)"
    cursor.execute(sql_cmd, {"sender": sender, "content": content, "timestamp": int(time.time()), "response_to": response_to})
    connection.commit()

app.run(port=5000, debug=True)