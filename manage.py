from manager import Manager

from wootowa import storage
from wootowa.app import app

manager = Manager()


@manager.command
def runserver():
    app.run("0.0.0.0")


@manager.command
def init_db():
    storage.init_db()


@manager.command
def drop_db():
    storage.drop_db()


if __name__ == "__main__":
    manager.main()
