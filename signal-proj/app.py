#!/usr/bin/env python
from flask import Flask, render_template, session, request
import flask as fl
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from sqlalchemy import create_engine

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

def init():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app, async_mode=async_mode)

    engine = create_engine('postgresql://localhost')

init()

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
