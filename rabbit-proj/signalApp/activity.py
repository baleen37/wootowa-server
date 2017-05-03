from .models import User
from .storage import db_session as db

class UserController(object):

    def create_user(self, form):
        user = User()
        user.nickname = form.get('nickname')
        user.password = form.get('nickname')

        db.add(user)
        db.commit()

        return user
