from flask import Flask, request, jsonify, render_template
import csv
import os
import hashlib

app = Flask(__name__)

#backend server for a chat app

def check_password(password, chat_id):
    #check if a user has the correct password for a chat
    file_path = "./server-py/data/" + chat_id + "/info.txt"
    chat_password = ""
    with open(file_path, 'r') as f:
        chat_password = f.read()
    
    if chat_password == "*":
        return True
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == chat_password #return true if the password is correct

def file_exists(file_path):
    try:
        with open(file_path, 'r') as f:
            return True
    except:
        return False

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/main.js')
def serve_js():
    return app.send_static_file('main.js'), {'Content-Type': 'text/javascript'}




@app.route('/send', methods=['POST'])
def send():
    #get the chat id from the request
    chat_id = request.form['chat_id']
    sender = request.form['sender']
    message = request.form['message']
    timestamp = request.form['timestamp']
    password = request.form['password']
    
    if not check_password(password, chat_id):
        return "wrong password", 401
    if not file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat does not exist", 404
    else:
        file_path = "./server-py/data/" + chat_id + "/chat.csv"
        
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([sender, message, timestamp])
        
        return "success", 200
    

@app.route("/new_chat", methods=['POST'])
def new_chat():
    chat_id = request.form["chat_id"]
    password = request.form["password"]
    if password in ["", " ", "*"]:
        password = "*"
    else:
        password = hashlib.sha256(password.encode()).hexdigest()
    
    if file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat already exists", 409
    
    file_path = "./server-py/data/"
    os.mkdir(file_path + chat_id)
    
    with open(file_path + chat_id + "/info.txt", 'w') as f:
        f.write(password)
    
    with open(file_path + chat_id + "/chat.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["sender", "message", "timestamp"])
    
    
    
    return "success", 200


@app.route('/get', methods=['POST'])
def get():
    #get the chat id from the request
    
    chat_id = request.form['chat_id']
    password = request.form['password']
    if not check_password(password, chat_id):
        return "wrong password", 401
    if not file_exists("./server-py/data/" + chat_id + "/info.txt"):
        return "chat does not exist", 404
    else:
        file_path = "./server-py/data/" + chat_id + "/chat.csv"
        
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        return jsonify(data), 200


@app.route("/clear", methods=['POST'])
def clear():
    chat_id = request.form['chat_id']
    password = request.form['password']
    if not check_password(password, chat_id):
        #return status code 401
        return "wrong password", 401
    else:
        #delete chat folder
        chat_folder = "./server-py/data/" + chat_id
        
        for file in os.listdir(chat_folder):
            os.remove(chat_folder + "/" + file)
        
        os.rmdir(chat_folder)
        
        return "success", 200



if __name__ == "__main__":
    app.run(debug=True)
