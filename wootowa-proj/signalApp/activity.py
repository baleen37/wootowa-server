from .models import User
from .storage import db_session as db

class UserController(object):

    @classmethod
    def get_or_create_user(self, form):
        device_id = form.get('device_id')
        user = self.get_user(device_id)

        if not user:
            user = User()
            user.device_id = device_id

        user.gender = User.Gender(int(form.get('gender')))
        user.age = form.get('age')

        db.add(user)
        db.commit()

        return user

    @classmethod
    def get_user(self, device_id):
        user = (db.query(User)
                .filter(User.device_id==device_id)
                .first())

        return user

    #@classmethod
    #def verify_user(self, name, password):
    #    hash_pw = User.new_password(password)

    #    q = (db.query(User)
    #         .filter(User.name==name)
    #         .filter(User.password==hash_pw))

    #    return db.query(q.exists()).scalar()

