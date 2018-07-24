# Project 2

Web Programming with Python and JavaScript

Chatbox: website where people can send messages and recieve them. Website carries up to a 100 messages in channels, which are created and shared by users.
user is able to change the background color of the chat.

index.js:
Javascript file to make the website interactive, takes user input and communicates with application.py and exchange data using socket.io
client stores client name and current channel

index.html:
Sets up the structure for the web program.

application.py:
server store messages within channels
returns messages to index.js

the website doesn't change channels immediately, I'm not sure where the problem lies because the javascript gets the channel change