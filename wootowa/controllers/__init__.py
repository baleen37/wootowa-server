from sqlalchemy.orm import Session


class BaseController:
    def __init__(self, db: Session):
        self.db = db
