from wootowa.glb.model.user import User


class UserController(object):
    @classmethod
    def get_or_create_user(cls, form):
        device_id = form.get('device_id')
        user = cls.get_user(device_id)

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
                .filter(User.device_id == device_id)
                .first())

        return user
