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

current_page = "general"

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
    channel = data["channel"]
    t = time.asctime( time.localtime(time.time()) )
    message = text + " (" + str(t) + ")"
    msg_list = channel_list[channel]
    msg_list.append(message)
    while len(msg_list) > 100:
        del msg_list[0]
    channel_list[channel] = msg_list
    emit("announce message", {"message": message}, broadcast=True)



@socketio.on("current page")
def page(data):
    page = data["page"]
    current_page = page
    emit("current channel", {"current_page": current_page}, broadcast=True)


@app.route("/messages", methods=["POST"])
def messages():

    # Get start and end point for posts to generate.
    start = int(request.form.get("start") or 0)
    end = int(request.form.get("end") or (start + 9))

    # Generate list of posts.
    data = []
    for i in range(start, end + 1):
        if len(channel_list[page]) >= i:
            data.append(channel_list[page][i])

    # Artificially delay speed of response.
    time.sleep(1)

    # Return list of posts.
    return jsonify(data)
