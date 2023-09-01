from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for
from dataclasses import dataclass
import os
import time
import csv
import sqlite3
import requests
import hashlib
from typing import TypedDict, List, Dict, Union

app = Flask(__name__)
connection = sqlite3.connect("data/database.db", check_same_thread=False)
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

def find_highest_chat_id():
    cursor = connection.cursor()
    cursor.execute("SELECT chat_id FROM chats")
    chat_ids = cursor.fetchall()
    chat_ids = [int(c[0]) for c in chat_ids]
    if len(chat_ids) == 0:
        return 0
    else:
        return max(chat_ids)

def find_chat_id(chat_name):
    curser = connection.cursor()
    cursor.execute("SELECT chat_id FROM chats WHERE chat_name = :chat_name", {"chat_name": chat_name})
    chat_id = cursor.fetchone()
    if chat_id == None:
        return None
    else:
        return chat_id[0]

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

    def __eq__(self, __value: object) -> bool:
        return self.text == __value.text
    
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


def load_chat(chat_id) -> "Chat":
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM chats WHERE chat_id = :chat_id", {"chat_id": chat_id})
    chat = cursor.fetchone()
    if chat == None:
        return None
    chat = Chat(chat[1], chat[2])
    chat.chat_id = chat_id
    chat.users = chat[3]
    chat.admins = chat[4]
    return chat

class Chat:
    def __init__(self, chat_name, chat_password = "*") -> None:
        self.chat_name: str = chat_name
        self.chat_password: str = chat_password
        self.users = []
        self.admins = []
        self.messages = []
        self.chat_id = 0
        self.last_send = int(time.time())
        self.last_access = int(time.time())

    def load(self, chat_id = None):
        connection = sqlite3.connect("data/database.db", check_same_thread=False)
        cursor = connection.cursor()
        chat_id = find_chat_id(self.chat_name) if chat_id == None else chat_id
        if chat_id == None:
            return None, 404
        sql_cmd = "SELECT * FROM messages" + str(chat_id)
        self.chat_id = chat_id
        cursor.execute(sql_cmd)
        messages = cursor.fetchall()
        messages = [Message(m[0], m[1], m[2], m[3], m[4]) for m in messages]
        self.messages = messages
        self.last_access = int(time.time())
        print("loaded chat " + str(self.chat_id))
        return self, 200
    
    def create(self, chat_name, chat_password):
        connection = sqlite3.connect("data/database.db", check_same_thread=False)
        cursor = connection.cursor()
        self.chat_name = chat_name
        self.chat_password = str(Encrypted_text().encrypt(chat_password, 5))
        self.chat_id = find_highest_chat_id() + 1
        sql_cmd = "CREATE TABLE IF NOT EXISTS messages" + str(self.chat_id) + " (message_id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, content TEXT, timestamp INTEGER, response_to INTEGER)"
        cursor.execute(sql_cmd)
        connection.commit()
    
    
    
    def append_message(self, message: "Message"):
        sql_cmd = "INSERT INTO messages" + str(self.chat_id) + " (sender, content, timestamp, response_to) VALUES (:sender, :content, :timestamp, :response_to)"
        connection = sqlite3.connect("data/database.db", check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(sql_cmd, {"sender": message.sender, "content": message.content, "timestamp": message.timestamp, "response_to": message.response_to})
        connection.commit()
        connection.close()
        self.messages.append(message)
        self.last_send = int(time.time())
    
    def append_user(self, user):
        user_id = user.user_id
        self.users.append(user_id)
        cursor.execute("UPDATE chats SET users = :users WHERE chat_id = :chat_id", {"users": str(self.users), "chat_id": self.chat_id})
        connection.commit()
    
    def check_password(self, password):
        print(self.chat_name, str(Encrypted_text().decrypt(self.chat_password, password)))
        return self.chat_name == str(Encrypted_text().decrypt(self.chat_password, password))

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
        self.last_access = int(time.time())
        return j


class Message:
    def __init__(self, message_id, sender, content, timestamp = None,  response_to = None):
        self.message_id = message_id
        self.sender = sender
        self.content = content
        self.timestamp = int(time.time()) if timestamp == None else timestamp
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

global chat_dict
chat_dict: Dict[int, Chat] = {} #chat_id: Chat

def filter_chat_dict():
    global chat_dict
    for chat_id in chat_dict:
        if int(time.time()) - chat_dict[chat_id].last_access > 60:
            chat_dict.pop(chat_id)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:path>")
def static_files(path):
    print("serving " + path)
    return send_from_directory("static", path)

#temporary
@app.route("/api/static/<path:path>")
def static_files_api(path):
    return send_from_directory("static", path), 200

@app.route("/api/ping")
def ping():
    return jsonify({"success": True}), 200




@app.route("/api/get_chat/<chat_id>")
def get_chat(chat_id):
    global chat_dict
    
    if chat_id in chat_dict:
        return jsonify(chat_dict[chat_id].to_json()), 200
        filter_chat_dict()
    else:
        try:
            chat, err_code = Chat(chat_id, "*").load(chat_id=chat_id)
        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Chat not found"}), 404
        if err_code == 404:
            return jsonify({"success": False, "error": "Chat not found"}), 404
        chat_dict[chat_id] = chat
        return jsonify(chat_dict[chat_id].to_json()), 200        



@app.route("/api/get_chat_length/<chat_id>")
def get_chat_length(chat_id):
    global chat_dict
    
    if chat_id in chat_dict:
        return_str = jsonify({"success": True, "length": len(chat_dict[chat_id].messages)})
        filter_chat_dict()
        return return_str, 200
        
    else:
        try:
            chat, err_code = Chat(chat_id, "*").load(chat_id=chat_id)
        except Exception as e:
            print(e)
            return jsonify({"success": False, "error": "Chat not found"}), 404
        if err_code == 404:
            return jsonify({"success": False, "error": "Chat not found"}), 404
        chat_dict[chat_id] = chat
        return jsonify({"success": True, "length": len(chat.messages)}), 200

@app.route("/api/create_chat/<chat_name>/<chat_password>")
def create_chat(chat_name, chat_password):
    global chat_dict
    filter_chat_dict()
    chat_id = find_chat_id(chat_name)
    if chat_id != None:
        return jsonify({"success": False, "error": "Chat already exists"}), 400
    chat = Chat(chat_name, chat_password)
    chat_dict[chat.chat_id] = chat
    chat.create(chat_name, chat_password)
    return jsonify({"success": True, "chat_id": chat.chat_id}), 200

@app.route("/api/send_message", methods=["POST"])
def send_message():

    data = request.get_json()
    chat_id = data["chat_id"]
    chat_password = data.get("chat_password", "*")
    sender = data["sender"]
    content = data["content"]
    response_to = data["response_to"] if "response_to" in data else None
    
    global chat_dict
    
    
    if chat_id not in chat_dict:
        chat, err_code = Chat(chat_id, "*").load(chat_id=chat_id)
        if err_code == 404:
            return jsonify({"success": False, "error": "Chat not found"}), 404
        chat_dict[chat_id] = chat 
    chat_dict[chat_id].append_message(Message(None, sender, content, response_to=response_to))
    filter_chat_dict()
    return jsonify({"success": True}), 200


#run without multithreading
app.run(host="0.0.0.0", port=80, threaded=False)