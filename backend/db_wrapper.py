
from dataclasses import dataclass
import sqlite3
import time
import uuid


def generate_id():
    return str(uuid.uuid4())


def _try(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs), True
        except Exception as e:
            return e, False
    return wrapper


def _time(func):
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        time_ms = (time.time() - start) * 1000
        print(f"{func.__name__} took {time_ms:.2f}ms")
        return result
    return wrapper


@dataclass
class User:
    id: str
    name: str
    password: str

    @staticmethod
    def get_random():
        random_id = generate_id()
        return User(random_id, f"User{random_id[:8]}", random_id[:8])
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password
        }


@dataclass
class Message:
    id: str
    sender_id: str
    content: str

    @staticmethod
    def get_random(sender_id: str):
        random_id = generate_id()
        return Message(random_id, sender_id, f"Message{random_id[:8]}")
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content
        }

@dataclass
class Chat:
    id: str
    user_ids: list[str]
    message_ids: list[Message]

    @staticmethod
    def get_random(user_ids: list[str]):
        random_id = generate_id()
        return Chat(random_id, user_ids, [])
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_ids": self.user_ids,
            "message_ids": self.message_ids
        }

class DB:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, db_path: str = "db.sqlite3"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.setup_tables()
    
    def setup_tables(self):
        py_to_sql_types = {
            str: "TEXT",
            int: "INTEGER",
            list: "TEXT"
        }

        u = User("", "", "")
        m = Message("", "", "")
        c = Chat("", [], [])

        for obj in [u, m, c]:
            class_name = obj.__class__.__name__

            attrs = [attr for attr in obj.__dict__.keys() if not attr.startswith("__")]

            sql_types = [py_to_sql_types[type(getattr(obj, attr))] for attr in attrs]

            sql_attrs = ""
            for i in range(len(attrs)):
                if attrs[i] == "id":
                    sql_attrs += f"{attrs[i]} TEXT PRIMARY KEY UNIQUE"
                elif attrs[i] == "name":
                    sql_attrs += f"{attrs[i]} TEXT UNIQUE"
                else:
                    sql_attrs += f"{attrs[i]} {sql_types[i]}"
                if i != len(attrs) - 1:
                    sql_attrs += ", "
            
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {class_name} ({sql_attrs})")
            self.conn.commit()
                

    @_try
    def add_user(self, user: User):
        r, s = self.get_user_by_name(user.name)
        print(r, s)
        if s:
            raise Exception("User already exists")
        
        self.cursor.execute("INSERT INTO User VALUES (?, ?, ?)", (user.id, user.name, user.password))
        self.conn.commit()
    
    @_try
    def get_user(self, user_id: str) -> User:
        self.cursor.execute("SELECT * FROM User WHERE id=?", (user_id,))
        return User(*self.cursor.fetchone())
    
    @_try
    def get_users(self) -> list[User]:
        self.cursor.execute("SELECT * FROM User")
        return [User(*user) for user in self.cursor.fetchall()]
    
    @_try
    def get_user_by_name(self, name: str) -> User:
        self.cursor.execute("SELECT * FROM User WHERE name=?", (name,))
        return User(*self.cursor.fetchone())
    
    @_try
    def search_users(self, name: str) -> list[User]:
        self.cursor.execute("SELECT * FROM User WHERE name LIKE ?", (f"%{name}%",))
        return [User(*user) for user in self.cursor.fetchall()]
    


    def delete_user(self, user_id: str):
        self.cursor.execute("DELETE FROM User WHERE id=?", (user_id,))
        self.conn.commit()
    
    def update_user(self, user: User):
        self.cursor.execute("UPDATE User SET name=?, password=? WHERE id=?", (user.name, user.password, user.id))
        self.conn.commit()
    
    
    

    def add_message(self, message: Message):
        self.cursor.execute("INSERT INTO Message VALUES (?, ?, ?)", (message.id, message.sender_id, message.content))
        self.conn.commit()

    @_try
    def get_message(self, message_id: str) -> Message:
        self.cursor.execute("SELECT * FROM Message WHERE id=?", (message_id,))
        return Message(*self.cursor.fetchone())
    
    @_try
    def get_messages_from_chat(self, chat_id: str) -> list[Message]:
        self.cursor.execute("SELECT message_ids FROM Chat WHERE id=?", (chat_id,))
        message_ids = self.cursor.fetchone()[0].split(";")
        messages = []
        for message_id in message_ids:
            self.cursor.execute("SELECT * FROM Message WHERE id=?", (message_id,))
            messages.append(Message(*self.cursor.fetchone()))
        return messages

    def delete_message(self, message_id: str):
        self.cursor.execute("DELETE FROM Message WHERE id=?", (message_id,))
        self.conn.commit()
    
    def update_message(self, message: Message):
        self.cursor.execute("UPDATE Message SET content=? WHERE id=?", (message.content, message.id))
        self.conn.commit()
    


    def add_chat(self, chat: Chat):
        user_ids_str = ";".join(chat.user_ids)
        message_ids_str = ";".join(chat.message_ids)

        self.cursor.execute("INSERT INTO Chat VALUES (?, ?, ?)", (chat.id, user_ids_str, message_ids_str))
        self.conn.commit()
    
    @_try
    def get_chat(self, chat_id: str) -> Chat:
        self.cursor.execute("SELECT * FROM Chat WHERE id=?", (chat_id,))
        chat = self.cursor.fetchone()
        return Chat(chat[0], chat[1].split(";"), chat[2].split(";"))
    
    @_try
    def get_chats_from_user(self, user_id: str) -> list[Chat]:
        self.cursor.execute("SELECT * FROM Chat")
        chats = self.cursor.fetchall()
        user_chats = []
        for chat in chats:
            if user_id in chat[1].split(";"):
                user_chats.append(Chat(chat[0], chat[1].split(";"), chat[2].split(";")))
        return user_chats
    
    @_try
    def get_all_chats(self) -> list[Chat]:
        self.cursor.execute("SELECT * FROM Chat")
        chats = self.cursor.fetchall()
        return [Chat(chat[0], chat[1].split(";"), chat[2].split(";")) for chat in chats]
    
    def delete_chat(self, chat_id: str):
        self.cursor.execute("DELETE FROM Chat WHERE id=?", (chat_id,))
        self.conn.commit()
    
    def update_chat(self, chat: Chat):
        user_ids_str = ";".join(chat.user_ids)
        message_ids_str = ";".join(chat.message_ids)

        self.cursor.execute("UPDATE Chat SET user_ids=?, message_ids=? WHERE id=?", (user_ids_str, message_ids_str, chat.id))
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.cursor.close()
