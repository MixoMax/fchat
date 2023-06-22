from main import app
import requests

#external_ip = requests.get('https://api.ipify.org').text
#print("External IP: " + external_ip)

app.run(host="0.0.0.0", port=80)