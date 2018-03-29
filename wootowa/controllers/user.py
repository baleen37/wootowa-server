from wootowa.controllers import BaseController
from wootowa.models import User


class UserController(BaseController):
    def create_user(self, username, password, nickname, birth_year):
        user = User(
            username=username,
            nickname=nickname,
            birth=birth_year
        )
        user.password = password
        return user
