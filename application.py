import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# list of all channels
channel_list = ['general']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel = request.form.get("channel")
        try:
            index_value = channel_list.index(channel)
        except ValueError:
            index_value = -1
        if index_value == -1:
            channel_list.append(channel)
    return render_template('index.html', channel_list=channel_list)


# @socketio.on("add channel")
# def add(data):
#     channel = data["channel"]
#     channel_list.append(channel)
#     emit("list channels", channel_list, broadcast=True)
