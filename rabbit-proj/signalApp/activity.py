from .models import User
from .storage import db_session as db

class UserController(object):

    def create_user(self, form):
        user = User()
        user.name = form.get('name') 
        user.password = User.new_password(form.get('password'))

        db.add(user)
        db.commit()

        return user

    def get_user(self, name):
        user = (db.query(User)
                .filter(User.name==name)
                .first())

        return user

    def verify_user(self, name, password):
        user = (db.query(User)
                .filter(User.name==name)
                .first())

        return user.verify_password(password)

