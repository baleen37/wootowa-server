import sys


def is_unittest():
    args = sys.argv
    if (arg in ['unittest', 'uwsgi'] for arg in args):
        return True

    return False
