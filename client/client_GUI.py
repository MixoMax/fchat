from typing import Optional
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QScrollArea
from PySide6.QtGui import QIcon, QFont
import client_core as core

import threading
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
        
        #scrollable chat history in the middle
        self.chat_history_widget = QScrollArea()
        self.chat_history_layout = QVBoxLayout()
        self.chat_history_widget.setWidgetResizable(True)
        self.chat_history_widget.setLayout(self.chat_history_layout)

        self.chat_history_widget.setWidgetResizable(True)
        self.chat_history_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.chat_history_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_history_widget.setWidget(QWidget())
        
        self.chat_history_widget.widget().setLayout(self.chat_history_layout)
        
        
        
        
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
        
        self.last_sender = ""
        
    def refresh_chat(self, scroll_to_bottom: bool = True):
        #get server url from input field
        server_url = "http://" + self.server_url_input.text()
        #get chat id from input field
        chat_id = self.chat_id_input.text()
        #get username from input field
        username = self.username_input.text()
        
        if self.server_url_input.text() == "":
            return
        if self.chat_id_input.text() == "":
            return
        
        self.chat = core.Chat(server_url)
        self.chat.change_chat_id(chat_id)
        self.chat.set_username(username)
        messages = self.chat.get_messages()
        
        self.clear_chat_history()
        
        for message in messages:
            self.add_message_to_chat_history(message)
        
        if scroll_to_bottom:
            #scroll to the bottom of the chat history
            self.chat_history_widget.verticalScrollBar().setValue(self.chat_history_widget.verticalScrollBar().maximum())
            
        self.chat_history_widget.update()
    
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
            timestamp = str(int(timedelta // 60)) + " minutes ago"
        elif timedelta < 86400:
            timestamp = str(int(timedelta // 3600)) + " hours ago"
        else:
            timestamp = str(int(timedelta // 86400)) + " days ago"
        
        message_widget = QWidget()
        message_layout = QVBoxLayout()
        #top: sender and timestamp
        #sender in the top left, timestamp in the top right
        #bottom: message content
        message_widget.setLayout(message_layout)
        
        
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        
        if sender == self.last_sender:
            sender_label = QLabel("")
        else:
            sender_label = QLabel(sender)
        sender_label.setFont(QFont("Arial", 12))
        sender_label.setMaximumWidth(100)
        
        #sender name should be in the top left corner
        sender_label.setStyleSheet("""
                                    position: absolute;
                                    top: 8px;
                                    left: 8px;
                                   """)
        
        sender_label.setAlignment(Qt.AlignLeft)
        sender_label.update()
        
        self.last_sender = sender
        
        top_layout.addWidget(sender_label)
        
        timestamp_label = QLabel(timestamp)
        timestamp_label.setFont(QFont("Arial", 8))
        
        timestamp_label.setStyleSheet("""
                                        position: absolute;
                                        top: 8px;
                                        right: 8px;
                                    """)
        
        top_layout.addWidget(timestamp_label)
        
        top_layout.setAlignment(Qt.AlignTop)
        
        top_widget.setLayout(top_layout)
        
        top_widget.setStyleSheet("""
                                border-radius: 15px;
                                padding: 5px;
                                margin: 5px;
                                
                                """)
        
        
        
        content_wraped = "\n".join(content[i:i+35] for i in range(0, len(content), 35))
        
        content_label = QLabel(content_wraped)
        content_label.setFont(QFont("Arial", 12))
        content_label.setWordWrap(True)
        
        
        message_layout.addWidget(top_widget)
        message_layout.addWidget(content_label)
        
        
        
        if sender == self.username_input.text():
            color = "#008050"
        else:
            color = "#ababc4"
            
        message_widget.setStyleSheet(f"""
                                    border-radius: 15px;
                                    padding: 5px;
                                    margin: 5px;
                                    background-color: {color};
                                    """)
        
        message_widget.update()
        
        self.chat_history_layout.addWidget(message_widget)
    
    def send(self):
        #get message from input field
        message = self.message_input.text()
        
        #get username from input field
        username = self.username_input.text()
        if username == "":
            return
        
        #get server url from input field
        server_url = "http://" + self.server_url_input.text()
        
        chat_id = self.chat_id_input.text()
        
        chat = core.Chat(server_url)
        chat.change_chat_id(chat_id)
        chat.set_username(username)
        
        chat.send_message(message)

    def auto_refresh(self):
        self.refresh_chat(False)
        QTimer.singleShot(1000, self.auto_refresh)

if __name__ == "__main__":
    app = QApplication([])
    window = Chat_Windows()
    window.auto_refresh()
    window.show()
    app.exec()