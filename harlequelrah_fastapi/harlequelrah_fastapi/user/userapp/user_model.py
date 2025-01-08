# from myproject.settings.database import Base, authentication
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from harlequelrah_fastapi.user import models
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer
from harlequelrah_fastapi.authorization.role_model import RoleModel
from harlequelrah_fastapi.authorization.privilege_model import PrivilegeModel
from sqlalchemy.orm import relationship

class User(Base, models.User):
    __tablename__ = "users"
    roles = relationship("Role", secondary="user_roles")


class Privilege(PrivilegeModel):
    __tablename__ = "privileges"
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="privileges")


class Role(RoleModel):
    __tablename__ = "roles"
    users = relationship("User", secondary="user_roles")
    privileges = relationship("Privilege", back_populates="role")


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
    )


authentication.User = User
metadata= Base.metadata
