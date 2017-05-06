#!/usr/bin/env python
import sys
from signalApp.app import socketio, app
from signalApp.storage import init_db

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('python manage.py [runserver, initdb]')

    command = sys.argv[1]
    if command == 'runserver':
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)

    if command == 'initdb':
        init_db()
