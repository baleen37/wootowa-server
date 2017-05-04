#!/usr/bin/env python
import functools
import flask_socketio as sio
from flask import (
    Flask, render_template, session, request,
    jsonify, make_response
)
from .storage import init_session, db_session
from .helpers.socket import SocketManager

from glb import config

from .models import User
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

def requires_auth(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        header = request.headers.get('Authorization')
        if header:
            _, token = header.split()
            resp = User.decode_auth_token(token)

            if isinstance(resp, Exception):
                return make_response(jsonify({
                    'msg': 'Required auth token',
                    'code': ApiCode.Failure.value
                })), 401

            request.user_id = resp
        else:
            return make_response(jsonify({
                'msg': 'Required auth token',
                'code': ApiCode.Failure.value
            })), 401

        return f(*args, **kwargs)
    return wrapped

@app.route('/v1/test', methods=['POST'])
@requires_auth
def api_test():
    return make_response(jsonify({
        'msg': request.user_id,
        'code': ApiCode.Success.value
    })), 201

@app.route('/v1/user/sign_in', methods=['POST'])
def sign_in():
    user_dict = request.form.to_dict()
    name = user_dict['name']
    pw = user_dict['password']

    result = UserController.verify_user(name, pw)

    if result:
        user = UserController.get_user(name)

        auth_token = user.encode_auth_token()
        responseObject = {
            'auth_token': auth_token.decode()
        }
        return make_response(jsonify({
                'data': responseObject,
                'msg': 'success',
                'code': ApiCode.Success.value
            })), 201
    else:
        return make_response(jsonify({
            'msg': 'failure',
            'code': ApiCode.Failure.value
        })), 401

@app.route('/v1/user/sign_up', methods=['POST'])
def sign_up():
    user_dict = request.form.to_dict()
    UserController().create_user(user_dict)
    return make_response(jsonify({
        'msg': 'success',
        'code': ApiCode.Failure.value
    })), 201

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
