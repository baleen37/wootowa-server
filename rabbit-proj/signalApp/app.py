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

from .models import (
    User
)
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
        #header에 있거나
        header = request.headers.get('Authorization')
        if header:
            _, token = header.split()
        else:
            #params로 있거나
            token = request.args.get('auth_token')

        if token:
            resp = User.decode_auth_token(token)

            if isinstance(resp, Exception):
                return make_response(jsonify({
                    'msg': 'Required auth token',
                    'code': ApiCode.Failure.value
                })), 401

            request.uid = resp
        else:
            return make_response(jsonify({
                'msg': 'Required auth token',
                'code': ApiCode.Failure.value
            })), 401

        return f(*args, **kwargs)
    return wrapped

@app.route('/streams.json', methods=['GET'])
def streams():
    streams = []
    for awaiter in manager.get_awaiter_list():
        streams.append({'name': awaiter, 'id': awaiter})
    return make_response(jsonify(streams)), 200

@app.route('/v1/test', methods=['POST'])
@requires_auth
def api_test():
    return make_response(jsonify({
        'msg': request.uid, 'code': ApiCode.Success.value
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
#@requires_auth
def connect():
    sio.emit('id', request.sid)
    print('connect client_id {}'.format(request.sid))

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
    manager.remove_awaiter(request.sid)

@socketio.on('init')
def init(data):
    print('init {}'.format(data))

@socketio.on('offer')
def offer(data):
    print('offer {}'.format(data))

@socketio.on('answer')
def answer(data):
    print('answer {}'.format(data))

@socketio.on('candidate')
def candidate(data):
    print('candidate {}'.format(data))

@socketio.on('readyToStream')
def ready_to_stream(data):
    print('ready_to_stream {}'.format(data))
    manager.add_awaiter(request.sid)

    for awaiter in manager.get_awaiter_list():
        if request.sid != awaiter:
            sio.emit('message', 
                     { 'type': 'init', 'from': request.sid }, room=awaiter )
            print('matching : from {} to {}'.format(request.sid, awaiter))
            manager.remove_awaiter(awaiter)
            manager.remove_awaiter(request.sid)
            break

@socketio.on('findRoom')
def findRoom(data):
    print('findRoom :' + request.sid)

@socketio.on('message')
def message(message):
    print('message() : {}'.format(message))
    to = message.get('to', None)

    if not to in manager.get_clients():
        return

    message.pop('to')
    message['from'] = request.sid

    print('message {}, room={}'.format(message, to))
    sio.emit('message', message, room=to)

@socketio.on('leave')
def leave():
    print('leave')

@socketio.on('ping')
def ping():
    sio.emit('pong')

@socketio.on_error_default
def default_error_handler(e):
    print(e)

@socketio.on_error()
def error_handler(e):
    print(e)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
