import requests
import time

#disable ipv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False

def send_message(message) -> None:
    """Send a message to the server"""
    #send a message to the server
    url = "http://localhost:80/api/send_message"
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    payload = {
        "chat_id": "2",
        "chat_password": "*",
        "sender": "py-test",
        "content": message
    }
    r = requests.post(url, headers=header, json=payload)
    print(r.text)
    print(r.status_code)

if __name__ == "__main__":
    t1 = time.perf_counter()
    send_message("Hello from python")
    print(f"Time: {time.perf_counter() - t1} seconds")