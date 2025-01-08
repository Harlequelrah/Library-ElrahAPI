# from myproject.settings.database import Base, authentication
from sqlalchemy import Column, ForeignKey, Integer, Table
from harlequelrah_fastapi.user import models
from sqlalchemy.orm import relationship
from .authorization_model import Role

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
    )
class User(Base, models.User):
    __tablename__ = "users"
    roles = relationship("Role", secondary="user_roles")


authentication.User = User
