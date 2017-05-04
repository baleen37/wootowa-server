#!/usr/bin/env python
import functools
import flask_socketio as sio
import flask as fl
from flask import Flask, render_template, session, request
from .storage import init_session, db_session
from .helpers.socket import SocketManager
from glb import config

from .models import *
from .activity import UserController
from .storage import db_session 
from .helpers.apicode import ApiCode

async_mode = None

app = Flask(__name__)
app.config.from_object(config)
manager = SocketManager()
socketio = sio.SocketIO(app, 
                        client_manager=manager,
                        ping_timeout=10,
                        ping_interval=1)
init_session(app)

def login_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapped

@app.route('/v1/user/sign_in', methods=['POST'])
def sign_in():
    user_dict = request.form.to_dict()
    name = user_dict['name']
    pw = user_dict['password']

    result = UserController().verify_user(name, pw)
    if result:
        return fl.jsonify({
            'msg': 'success',
            'code': ApiCode.Success.value
        })
    else:
        return fl.jsonify({
            'msg': '실패',
            'code': ApiCode.Failure.value
        })

@app.route('/v1/user/sign_up', methods=['POST'])
def sign_up():
    user_dict = request.form.to_dict()
    UserController().create_user(user_dict)

    return fl.jsonify({
        'msg': 'success',
        'code': ApiCode.Success.value
    })

@socketio.on('connect')
def connect():
    client_id = request.sid
    sio.emit('id', client_id)
    print('client_id : {}'.format(client_id))
    print('auth_token : {}'.format(request.auth_token))

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
    participants = list(manager.get_participants('/', None))

    for p in participants:
        if p != request.sid:
            sio.emit('message', { 'from': p } )
            print('from : {}'.format(p))

    print('participants : {}'.format(participants))

@socketio.on('message')
def message(message):
    print('message {}'.format(message))

@socketio.on('update')
def update():
    print('update')

@socketio.on('leave')
def leave():
    print('leave')

@socketio.on('ping')
def ping():
    sio.emit('pong')

@socketio.on_error_default
def default_error_handler(e):
    print(e)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
