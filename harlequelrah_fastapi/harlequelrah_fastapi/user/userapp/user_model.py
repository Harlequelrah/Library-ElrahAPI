from settings.database import  Base
from harlequelrah_fastapi.user import models


class User(Base, models.User):
    __tablename__ = "users"
