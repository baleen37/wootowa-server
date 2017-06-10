#!/usr/bin/env python
import sys

from wootowa.signaling import app as signal_app
from wootowa.web import app as web_app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('python manage.py [runserver, initdb]')

    command = sys.argv[1]
    if command == 'runserver':
        argument = sys.argv[2]
        if argument == 'signal':
            signal_app.run()
        if argument == 'web':
            web_app.run()
