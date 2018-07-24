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

# temporary list to add message to a channel
msg_list = []

current_page = "general"


@app.route("/")
def index():
    return render_template('index.html', channel_list=channel_list)

# gets the name of the channel submitted by the user and broadcasts it
@socketio.on("submit channel")
def channel(data):
    global channel_list
    channel = data["channel"]

    # checks if channel already exists, if not add channel
    if channel not in channel_list.keys() and len(channel) != 0:
        channel_list[channel]=[]
    emit("announce channel", {"channel": channel}, broadcast=True)


# gets the name of the message submitted by the user and broadcasts it
@socketio.on("submit message")
def message(data):
    global channel_list, msg_list
    text = data["message"]
    channel = data["channel"]
    t = time.asctime( time.localtime(time.time()) )
    message = text + " (" + str(t) + ")"

    # adds message to channel list
    msg_list = channel_list[channel]
    msg_list.append(message)

    # checks if there are more than a 100 messages in the channel
    while len(msg_list) > 100:
        del msg_list[0]
    channel_list[channel] = msg_list
    emit("announce message", {"message": message}, broadcast=True)


# updates the current page variable
@socketio.on("current page")
def page(data):
    global current_page
    page = data["page"]
    current_page = page
    emit("current channel", {"current_page": current_page}, broadcast=True)


# loads messages
@app.route("/messages", methods=["POST"])
def messages():

    # get start and end point for messages to send
    start = int(request.form.get("start") or 0)
    end = int(request.form.get("end") or (start + 9))

    # generate list of messages
    data = []
    for i in range(start, end + 1):
        if len(channel_list[page]) >= i:
            data.append(channel_list[page][i])

    # return list of messages
    return jsonify(data)
