from flask import Flask, request, jsonify
from GcpDB import *
import os
from typing import TypedDict

app = Flask(__name__)

global user_session_dict
user_session_dict: dict[str, int] = {} # {session_id: user_id}

@app.route("/")
def index():
    return "This is the API version only, no GUI available."


#User handling
@app.route("/api/users/create", methods=["POST"])
def create_user():
    payload = request.get_json()
    if payload is None:
        return "No payload provided", 400
    if "username" in payload and "password" in payload:
        r = create_user_db(payload["username"], payload["password"], payload.get("email", ""))
        if r:
            return "User created", 200
        else:
            return "User already exists", 400
    else:
        return "Missing username or password", 400

@app.route("/api/users/login", methods=["POST"])
def login_user():
    payload = request.get_json()
    if payload is None:
        return "No payload provided", 400
    if "username" in payload and "password" in payload:
        if confirm_login(payload["username"], payload["password"]):
            session_id = os.urandom(16).hex()
            user_session_dict[session_id] = get_user_id(payload["username"])
            return jsonify({"session_id": session_id}), 200
        else:
            return "Wrong username or password", 400