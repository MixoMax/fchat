from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QIcon, QFont
import client_core as core

import time

class Chat_Windows(QMainWindow):
    chat = None
    def __init__(self):
        super().__init__()
        
        #set window title and size
        self.setWindowTitle("FChat")
        self.setMinimumSize(800, 600)
        
        #server url, chat id and username input fields at the top
        #scrollable chat history in the middle
        #message input field, send button and refresh button at the bottom
        
        #top part
        self.top_widget = QWidget()
        self.top_layout = QFormLayout()
        self.top_widget.setLayout(self.top_layout)
        
        self.server_url_input = QLineEdit()
        self.server_url_input.setPlaceholderText("Server URL")
        self.top_layout.addRow(self.server_url_input)
        
        self.chat_id_input = QLineEdit()
        self.chat_id_input.setPlaceholderText("Chat ID")
        self.top_layout.addRow(self.chat_id_input)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.top_layout.addRow(self.username_input)
        
        #middle part
        self.chat_history_widget = QWidget()
        self.chat_history_layout = QVBoxLayout()
        self.chat_history_widget.setLayout(self.chat_history_layout)
        
        #bottom part
        #message input field in the left / middle, send and refresh buttons in the right
        self.bottom_widget = QWidget()
        self.bottom_layout = QHBoxLayout()
        self.bottom_widget.setLayout(self.bottom_layout)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message")
        self.bottom_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.bottom_layout.addWidget(self.send_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.bottom_layout.addWidget(self.refresh_button)
    
        #add all parts to the main window
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.chat_history_widget)
        self.main_layout.addWidget(self.bottom_widget)
        
        self.setCentralWidget(self.main_widget)
        
        #connect buttons to functions
        self.send_button.clicked.connect(self.send)
        self.refresh_button.clicked.connect(self.refresh_chat)
        
    def refresh_chat(self):
        #get server url from input field
        server_url = "http://" + self.server_url_input.text()
        #get chat id from input field
        chat_id = self.chat_id_input.text()
        #get username from input field
        username = self.username_input.text()
        
        self.chat = core.Chat(server_url)
        self.chat.change_chat_id(chat_id)
        self.chat.set_username(username)
        messages = self.chat.get_messages()
        
        self.clear_chat_history()
        
        for message in messages:
            self.add_message_to_chat_history(message)
    
    def clear_chat_history(self):
        for i in reversed(range(self.chat_history_layout.count())):
            self.chat_history_layout.itemAt(i).widget().setParent(None)
    
    def add_message_to_chat_history(self, message: core.Message):
        content = message.content
        sender = message.sender
        timedelta = abs(message.timestamp - time.time())
        if timedelta < 60:
            timestamp = str(int(timedelta)) + " seconds ago"
        elif timedelta < 3600:
            timestamp = str(int(timedelta / 60)) + " minutes ago"
        elif timedelta < 86400:
            timestamp = str(int(timedelta / 3600)) + " hours ago"
        else:
            timestamp = str(int(timedelta / 86400)) + " days ago"
        
        message_widget = QWidget()
        message_layout = QHBoxLayout()
        message_widget.setLayout(message_layout)
        
        sender_label = QLabel(sender)
        sender_label.setFont(QFont("Arial", 12))
        message_layout.addWidget(sender_label)
        
        content_label = QLabel(content)
        content_label.setFont(QFont("Arial", 12))
        message_layout.addWidget(content_label)
        
        timestamp_label = QLabel(timestamp)
        timestamp_label.setFont(QFont("Arial", 12))
        message_layout.addWidget(timestamp_label)
        
        self.chat_history_layout.addWidget(message_widget)
        
    def send(self):
        #get message from input field
        message = self.message_input.text()
        
        #get username from input field
        username = self.username_input.text()
        
        #get server url from input field
        server_url = "http://" + self.server_url_input.text()
        
        chat_id = self.chat_id_input.text()
        
        chat = core.Chat(server_url)
        chat.change_chat_id(chat_id)
        chat.set_username(username)
        
        chat.send_message(message)

if __name__ == "__main__":
    app = QApplication([])
    window = Chat_Windows()
    window.show()
    app.exec()