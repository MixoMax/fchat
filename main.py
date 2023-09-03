from flask import Flask
from GcpDB import *
import os
from typing import TypedDict

app = Flask(__name__)

global user_session_dict
user_session_dict: dict[str, int] = {} # {session_id: user_id}

@app.route("/")
def index():
    return "This is the API version only, no GUI available."

