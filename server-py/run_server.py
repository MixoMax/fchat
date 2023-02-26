import waitress
from main import app
import requests
import socket

#get external ip
R = requests.get("http://ip-api.com/json").json()
IP = R["query"]
print("Running on: " + IP + ":80 (external ip))")

#get internal ip
print("Running on: " + socket.gethostbyname(socket.gethostname()) + ":80 (internal ip))")


waitress.serve(app, host="127.0.0.1", port=80)
