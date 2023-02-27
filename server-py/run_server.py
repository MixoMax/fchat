import waitress
from main import app
import requests
import socket


port = 80

#get external ip
R = requests.get("http://ip-api.com/json").json()
IP = R["query"]
print("Running on: " + IP, ":", port, "(external ip)")

#get internal ip
print("Running on: " + socket.gethostbyname(socket.gethostname()), ":", port, "(internal ip)")



waitress.serve(app, listen="*" + ":" + str(port))
