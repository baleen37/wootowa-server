import socketio
from flask import Flask, render_template

from wootowa.glb import config

async_mode = None

# WSGI server
mgr = socketio.RedisManager(config.REDIS_URI)
sio = socketio.Server(async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)


@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('message')
def message(sid, data):
    print('message ', data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


@sio.on('join')
def enter_room(sid, data):
    sio.enter_room(sid, data['room'])


@sio.on('leave room')
def leave_room(sid, data):
    sio.leave_room(sid, data['room'])


def run():
    app.run(threaded=True, debug=True, port=8000)
