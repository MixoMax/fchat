from flask import Flask, request, jsonify, render_template
import csv
import os
import hashlib
import base64

app = Flask(__name__)

#backend server for a chat app

def check_password(password, chat_id):
    #check if a user has the correct password for a chat
    file_path = "./server-py/data/" + chat_id + "/info.txt"
    chat_password = ""
    try:
        with open(file_path, 'r') as f:
            chat_password = f.read()
    except:
        return False, 404
    
    if chat_password == "*":
        return True
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == chat_password, 401 #return true if the password is correct

def file_exists(file_path):
    try:
        with open(file_path, 'r') as f:
            return True
    except:
        return False


def encode(message):
    """Encode a chat message using Base64."""
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    encoded_message = base64_bytes.decode('utf-8')
    return encoded_message

def decode(encoded_message):
    """Decode a chat message that was previously encoded using Base64."""
    padding_needed = len(encoded_message) % 4
    if padding_needed > 0:
        encoded_message += '=' * (4 - padding_needed)
    base64_bytes = encoded_message.encode('utf-8')
    try:
        message_bytes = base64.b64decode(base64_bytes)
        decoded_message = message_bytes.decode('utf-8')
    except UnicodeDecodeError:
        message_bytes = base64.b64decode(base64_bytes)
        decoded_message = message_bytes.decode('latin-1', 'ignore')
    return decoded_message

    


@app.route("/", methods=['GET'])
def index():
    return render_template("login.html")

@app.route('/main.js')
def serve_js():
    return app.send_static_file('main.js'), {'Content-Type': 'text/javascript'}

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route("/stylesheet1.css")
def stylesheet1():
    return app.send_static_file("stylesheet1.css")

@app.route("/chat", methods=['GET'])
def chat():
    return render_template("chat.html")


@app.route("/media.mp4")
def media():
    return app.send_static_file("media.mp4")


@app.route('/send', methods=['POST'])
def send():
    #get the chat id from the request
    chat_id = request.form['chat_id']
    sender = request.form['sender']
    message = request.form['message']
    timestamp = request.form['timestamp']
    password = request.form['password']
    
    if not check_password(password, chat_id):
        return "wrong password", check_password(password, chat_id)[1] #unauthorized or not found
    if not file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat does not exist", 404 #not found
    else:
        file_path = "./server-py/data/" + chat_id + "/chat.csv"
        
        with open(file_path, 'a', newline="") as f:
            writer = csv.writer(f)
            sender = encode(sender)
            message = encode(message)
            writer.writerow([sender, message, timestamp])
        
        return "success", 200 #success
    

@app.route("/new_chat", methods=['POST'])
def new_chat():
    chat_id = request.form["chat_id"]
    password = request.form["password"]
    if password in ["", " ", "*"]:
        password = "*"
    else:
        password = hashlib.sha256(password.encode()).hexdigest()
    
    if file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat already exists", 409 #conflict
    
    file_path = "./server-py/data/"
    os.mkdir(file_path + chat_id)
    
    with open(file_path + chat_id + "/info.txt", 'w') as f:
        f.write(password)
    
    with open(file_path + chat_id + "/chat.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["sender", "message", "timestamp"])
    
    
    
    return "success", 200 #success


@app.route('/get', methods=['POST'])
def get():
    #get the chat id from the request
    
    chat_id = request.form['chat_id']
    password = request.form['password']
    if not check_password(password, chat_id):
        return "wrong password", check_password(password, chat_id)[1] #unauthorized or not found
    if not file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat does not exist", 404 #not found
    else:
        file_path = "./server-py/data/" + chat_id + "/chat.csv"
        
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        decoded_data = []
        for row in data:
            decoded_sender = decode(row[0])
            decoded_message = decode(row[1])
            if decoded_sender == "" and decoded_message == "":
                continue
            elif row[0] == "sender" and row[1] == "message" and row[2] == "timestamp":
                continue
            else:
                decoded_data.append([decoded_sender, decoded_message, row[2]])
            
            
        
        return jsonify(decoded_data), 200 #success


@app.route("/clear", methods=['POST'])
def clear():
    chat_id = request.form['chat_id']
    password = request.form['password']
    if not file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat does not exist", 404 #not found
    if not check_password(password, chat_id):
        return "wrong password", check_password(password, chat_id)[1] #unauthorized or not found
    else:
        #delete chat folder
        chat_folder = "./server-py/data/" + chat_id
        
        for file in os.listdir(chat_folder):
            os.remove(chat_folder + "/" + file)
        
        os.rmdir(chat_folder)
        
        return "success", 200 #success


@app.route("/teapot", methods=['GET'])
def i_am_a_teapot():
    return "I am a teapot", 418 #I am a teapot


if __name__ == "__main__":
    app.run(debug=True)
