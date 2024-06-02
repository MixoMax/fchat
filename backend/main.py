import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from db_wrapper import DB, User, Message, Chat, generate_id


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


db = DB(db_path="db.sqlite3")


class Auth:
    __keys: dict[str,tuple[str, int]] = {} # random_id: (user_id, expiration_time)

    tte = 60 * 60 * 24 # 24 hours

    def __init__(self):
        self.__keys = {}
    
    def generate_key(self, user_id: str) -> str:
        random_id = generate_id()
        self.__keys[random_id] = (user_id, int(time.time()) + self.tte)
        return random_id
    
    def validate_key(self, key: str, user_id: str) -> bool:
        if key not in self.__keys:
            # key not found
            return False
        
        if self.__keys[key][0] != user_id:
            # user_id does not match
            return False
        
        if self.__keys[key][1] < int(time.time()):
            # key expired
            del self.__keys[key]
            return False
        
        return True
    
    def delete_key(self, key: str):
        if key in self.__keys:
            del self.__keys[key]


auth = Auth()


@app.get("/users/auth")
def auth_user(password: str, user_id: str = None, name: str = None):
    if user_id:
        user, success = db.get_user(user_id)
    elif name:
        user, success = db.get_user_by_name(name)
    else:
        return JSONResponse(content={"error": "No user_id or name provided"}, status_code=400)

    if not success:
        return JSONResponse(content={"error": str(user)}, status_code=500)
    
    if user.password != password:
        return JSONResponse(content={"error": "Invalid password"}, status_code=401)
    
    key = auth.generate_key(user_id)
    return JSONResponse(content={"key": key})

@app.get("/users/create")
def create_user(name: str, password: str):
    user = User(generate_id(), name, password)
    err, success = db.add_user(user)

    print(success)

    if not success:
        return JSONResponse(content={"error": str(err)}, status_code=409) # 409 Conflict

    return JSONResponse(content={"user_id": user.id})

@app.get("/users/delete")
def delete_user(user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    db.delete_user(user_id)
    return JSONResponse(content={"success": True})

@app.get("/users/search")
def search_users(query: str = ""):
    users, success = db.search_users(query)

    if not success:
        return JSONResponse(content={"error": str(users)}, status_code=500)

    return JSONResponse(content={"users": [user.id for user in users]})




@app.post("/messages/add")
async def add_message(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    key = data["key"]
    content = data["content"]
    
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    message = Message(generate_id(), user_id, content)
    db.add_message(message)

    if "chat_id" in data:
        chat_id = data["chat_id"]
        chat, success = db.get_chat(chat_id)
        if not success:
            return JSONResponse(content={"error": str(chat)}, status_code=500)
        
        chat.message_ids.append(message.id)
        db.update_chat(chat)

    return JSONResponse(content={"success": success})

@app.get("/messages/delete")
def delete_message(message_id: str, user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    db.delete_message(message_id)
    return JSONResponse(content={"success": True})

@app.post("/messages/update")
async def update_message(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    key = data["key"]
    message_id = data["message_id"]
    content = data["content"]
    
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    message, success = db.get_message(message_id)
    if not success:
        return JSONResponse(content={"error": str(message)}, status_code=500)
    
    message.content = content
    db.update_message(message)
    return JSONResponse(content={"success": str(success)})


@app.get("/messages/get")
def get_message(message_id: str = None, chat_id: str = None):
    if message_id:
        message, success = db.get_message(message_id)
        if not success:
            return JSONResponse(content={"error": str(message)}, status_code=500)
        return JSONResponse(content={"message": message.to_dict()})
    
    if chat_id:
        chat, success = db.get_chat(chat_id)
        if not success:
            return JSONResponse(content={"error": str(chat)}, status_code=500)
        
        messages = []
        for message_id in chat.message_ids:
            message, success = db.get_message(message_id)
            if not success:
                return JSONResponse(content={"error": str(message)}, status_code=500)
            messages.append(message.to_dict())
        
        return JSONResponse(content={"messages": messages})

@app.get("/chats/get")
def get_chat(chat_id: str = None, user_id: str = None):
    if chat_id:
        chat, success = db.get_chat(chat_id)
        if not success:
            return JSONResponse(content={"error": str(chat)}, status_code=500)
        return JSONResponse(content={"chat": chat.to_dict()})
    
    if user_id:
        chats, success = db.get_chats_from_user(user_id)
        if not success:
            return JSONResponse(content={"error": str(chats)}, status_code=500)
        
        return JSONResponse(content={"chats": [chat.to_dict() for chat in chats]})
    
    chats, success = db.get_all_chats()
    if not success:
        return JSONResponse(content={"error": str(chats)}, status_code=500)
    
    return JSONResponse(content={"chats": [chat.to_dict() for chat in chats]})

@app.get("/chats/create")
def create_chat(user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    chat = Chat(generate_id(), [user_id], [])
    db.add_chat(chat)
    return JSONResponse(content={"chat_id": chat.id})

@app.get("/chats/delete")
def delete_chat(chat_id: str, user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    chat, success = db.get_chat(chat_id)
    if not success:
        return JSONResponse(content={"error": str(chat)}, status_code=500)
    
    if user_id not in chat.user_ids:
        return JSONResponse(content={"error": "User not in chat"}, status_code=401)
    
    db.delete_chat(chat_id)

    return JSONResponse(content={"success": True})

@app.get("/chats/add_user")
def add_user_to_chat(chat_id: str, user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    chat, success = db.get_chat(chat_id)
    if not success:
        return JSONResponse(content={"error": str(chat)}, status_code=500)
    
    chat.user_ids.append(user_id)
    db.update_chat(chat)

    return JSONResponse(content={"success": True})

@app.get("/chats/remove_user")
def remove_user_from_chat(chat_id: str, user_id: str, key: str):
    if not auth.validate_key(key, user_id):
        return JSONResponse(content={"error": "Invalid key"}, status_code=401)
    
    chat, success = db.get_chat(chat_id)
    if not success:
        return JSONResponse(content={"error": str(chat)}, status_code=500)
    
    if user_id not in chat.user_ids:
        return JSONResponse(content={"error": "User not in chat"}, status_code=401)
    
    chat.user_ids.remove(user_id)
    db.update_chat(chat)

    return JSONResponse(content={"success": True})

@app.get("/chats/exists")
def chat_exists(chat_id: str):
    chat, success = db.get_chat(chat_id)
    return JSONResponse(content={"exists": success})

@app.get("/favicon.ico")
def favicon():
    return FileResponse("./favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)