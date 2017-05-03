#!/usr/bin/env python
import flask as fl
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from sqlalchemy import create_engine

from .storage import engine
from .. import config

async_mode = None

app = Flask(__name__)
app.config = config
socketio = SocketIO(app, async_mode=async_mode)

engine = create_engine('postgresql://localhost')

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def connect():
    clientId = 'asdf';
    emit('id', clientId)
    print('id: {}'.format(clientId))

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('init')
def init():
    print('init')

@socketio.on('offer')
def offer():
    print('offer')

@socketio.on('answer')
def answer():
    print('answer')

@socketio.on('candidate')
def candidate():
    print('candidate')

@socketio.on('readyToStream')
def ready_to_stream(data):
    print('ready_to_stream {}'.format(data))
    send('init')

@socketio.on('message')
def message(message):
    print('message {}'.format(message))

@socketio.on('update')
def update():
    print('update')

@socketio.on('leave')
def leave():
    print('leave')

@socketio.on_error_default
def default_error_handler(e):
    print(e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)
