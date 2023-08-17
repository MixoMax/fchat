"""client core module to interact with an fchat server.
implements all the necessary functionality."""
import requests
import json

#disable ipv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False

class Message:
    message_id: int
    sender: str
    content: str
    timestamp: int
    response_to: int
    
    def from_dict(json) -> "Message":
        m = Message()
        m.content = json["content"]
        m.message_id = json["message_id"]
        m.response_to = json["response_to"]
        m.sender = json["sender"]
        m.timestamp = json["timestamp"]
        return m        
    
    def __str__(self) -> str:
        return f"{self.sender}: {self.content}"
    
    def __repr__(self) -> str:
        return f"<Message {self.message_id} | {self.sender}: {self.content}>"


class Chat:
    def __init__(self, url: str) -> None:
        self.url = url
        self.messages = []
        self.chat_id = "1"
        self.username = "anonymous"

    def __str__(self) -> str:
        return f"<Chat {self.url} | {len(self.messages)} messages>"

    def print_messages(self):
        self.get_chat()
        for message in self.messages:
            print(message.__str__())

    def _clear_messages(self):
        self.messages = []

    def change_chat_id(self, chat_id: str):
        self.chat_id = chat_id
        self._clear_messages()

    def set_username(self, username: str):
        self.username = username

    def get_chat(self):
        api_url = self.url + "/api/get_chat/" + self.chat_id
        r = requests.get(api_url).text
        r_json = json.loads(r)
        for elem in r_json:
            self.messages.append(Message.from_dict(elem))

    def get_messages(self):
        self.get_chat()
        return self.messages

    def create_chat(self, chat_name: str, chat_password: str):
        api_url = self.url + "/api/create_chat/" + chat_name + "/" + chat_password
        r = requests.get(api_url)

    def send_message(self, content: str, response_to: int = None):
        api_url = self.url + "/api/send_message"
        data = {
            "chat_id": self.chat_id,
            "sender": self.username,
            "content": content,
        }
        if response_to != None:
            data["response_to"] = response_to
        r = requests.post(api_url, json = data)
