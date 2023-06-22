from flask import Flask, jsonify, render_template, request
from dataclasses import dataclass
import os
import time
import csv
import requests
import hashlib

# TODO:
app = Flask(__name__)




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
        csv_path = "./data/users.csv"

        self.username = username
        self.password = password
        
        with open(csv_path, "r") as csv_file:
            csv_data = list(csv.reader(csv_file))
            self.user_id = csv_data[-1][0] + 1
        self.last_online = int(time.time())
        
        user_data = [self.user_id, self.username, self.password, self.last_online]
        with open(csv_path, "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(user_data)
        
    
    def __str__(self) -> str:
        return self.username
    
    def to_json(self):
        j = {
            "username": self.username,
            "user_id": self.user_id,
            "password": self.password,
            "last_online": self.last_online
        }
        return j
    
    def add_chat(self, chat):
        self.chats.append(chat)
    
    def update_last_online(self):
        self.last_online = int(time.time())

class Chat:
    def __init__(self):
        self.chat_name: str = ""
        self.chat_password: str = ""
        self.users = []
        self.messages = []
        
    def from_csv(self, csv_path):
        self.csv_path = csv_path
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    self.chat_id = row[0]
                    self.chat_name = row[1]
                    self.chat_password = row[2]
                else:
                    self.messages.append(row)
        
        return self
    
    def create(self, chat_id, chat_name, chat_password):
        self.chat_id = chat_id
        self.chat_name = chat_name
        self.chat_password = chat_password
        
        self.csv_path = "./data/chats/" + self.chat_id + ".csv"
        
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        
        with open(self.csv_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([self.chat_id, self.chat_name, self.chat_password])
        
        return self        
    
    def append_message(self, message):
        message_data = [message.message_id, message.sender, message.content, message.timestamp, message.response_to]
        self.messages.append(message_data)
        with open(self.csv_path, "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(message_data)
    
    def append_user(self, user):
        user_id = user.user_id
        self.users.append(user_id)

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
            "users": users
        }
        return j

class Message:
    def __init__(self, chat_id, sender, content, response_to = None):
        self.chat_id = chat_id
        self.sender = sender
        self.content = content
        self.timestamp = int(time.time())
        self.response_to = response_to
        
        csv_path = "./data/chats/" + chat_id + ".csv"
        
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        try:
            self.message_id = int(list(csv.reader(open(csv_path, "r")))[-1][0]) + 1
        except:
            self.message_id = 0
    
    
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
    chat_csv = "./data/chats/" + chat_id + ".csv"
    messages = []
    with open(chat_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            messages.append(row)
    
    return jsonify(messages)

@app.route("/api/create_chat/<chat_id>/<chat_name>/<chat_password>")
def create_chat(chat_id, chat_name, chat_password):
    chat = Chat().create(chat_id, chat_name, chat_password)
    return jsonify(chat.to_json())

@app.route("/api/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    chat_id = data["chat_id"]
    sender = data["sender"]
    content = data["content"]
    response_to = data["response_to"] if "response_to" in data else None
    
    m = Message(chat_id, sender, content, response_to)
    
    csv_path = "./data/chats/" + chat_id + ".csv"
    if os.path.exists(csv_path):
        c = Chat().from_csv(csv_path)
        c.append_message(m)
        return jsonify(m.to_json())
    else:
        return jsonify({"error": "Chat does not exist"})

app.run(port=5000, debug=True)