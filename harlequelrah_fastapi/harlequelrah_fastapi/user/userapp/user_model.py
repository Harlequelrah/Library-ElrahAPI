# from myproject.settings.database import Base, authentication
from harlequelrah_fastapi.user import models


class User(Base, models.User):
    __tablename__ = "users"


authentication.User = User
