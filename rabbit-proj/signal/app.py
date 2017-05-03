#!/usr/bin/env python
import functools
import socketio
import flask_socketio as sio
import flask as fl
from flask import Flask, render_template, session, request
from .storage import init_engine, init_session
from glb import config

async_mode = 'threading'

app = Flask(__name__)
app.config.from_object(config)
socketio = sio.SocketIO(app)
init_engine(app.config['RABBIT_DB'])
init_session(app)

def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapped

@app.route('/login', methods=['GET', 'POST'])
def login():
    return

@socketio.on('connect')
def connect():
    client_id = request.sid
    sio.emit('id', client_id)
    print('client_id : {}'.format(client_id))

@socketio.on('disconnect')
def disconnect():
    sio.disconnect()
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
    print('rooms : {}'.format(sio.rooms()))

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

