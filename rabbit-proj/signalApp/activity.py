from .models import User
from .storage import db_session as db

class UserController(object):

    @classmethod
    def create_user(self, form):
        user = User()
        user.name = form.get('name') 
        user.password = User.new_password(form.get('password'))

        db.add(user)
        db.commit()

        return user

    @classmethod
    def get_user(self, name):
        user = (db.query(User)
                .filter(User.name==name)
                .first())

        return user

    @classmethod
    def verify_user(self, name, password):
        hash_pw = User.new_password(password)

        q = (db.query(User)
             .filter(User.name==name)
             .filter(User.password==hash_pw))

        return db.query(q.exists()).scalar()

