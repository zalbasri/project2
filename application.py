import os
import requests
import time

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# list of all channels
channel_list = {'general':[]}

# temporary list
msg_list = []

@app.route("/")
def index():
    return render_template('index.html', channel_list=channel_list)

@socketio.on("submit channel")
def channel(data):
    channel = data["channel"]
    if channel not in channel_list.keys() and len(channel) != 0:
        channel_list[channel]=[]
    emit("announce channel", {"channel": channel}, broadcast=True)

@socketio.on("submit message")
def message(data):
    text = data["message"]
    t = time.asctime( time.localtime(time.time()) )
    message = text + " (" + str(t) + ")"
    msg_list = channel_list['general']
    msg_list.append(message)
    while len(msg_list) > 100:
        del msg_list[0]
    channel_list['general'] = msg_list
    emit("announce message", {"message": message}, broadcast=True)

