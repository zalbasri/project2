import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# list of all channels
channel_list = {'general':["banana", "apple"]}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel = request.form.get("channel")
        if channel not in channel_list.keys():
            channel_list[channel]=[]
    return render_template('index.html', channel_list=channel_list)

@app.route("/<string:channel>")
def channel():
    return channel_list.get(channel)

