from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

#backend server for a chat app


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
    
    file_path = "./server-py/data/" + chat_id + ".csv"
    
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([sender, message, timestamp])
    
    return "success"
    

@app.route("/new_chat", methods=['POST'])
def new_chat():
    chat_id = request.form["chat_id"]
    
    with open("./server-py/data/" + chat_id + ".csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sender', 'message'])
    
    return "success"


@app.route('/get', methods=['POST'])
def get():
    #get the chat id from the request
    
    chat_id = request.form['chat_id']
    
    file_path = "./server-py/data/" + chat_id + ".csv"
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    return jsonify(data)






if __name__ == "__main__":
    app.run(debug=True)
