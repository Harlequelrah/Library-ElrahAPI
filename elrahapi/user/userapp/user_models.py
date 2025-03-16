from myproject.settings.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from elrahapi.user.models import UserModel
from  elrahapi.authorization.user_privilege_model import UserPrivilegeModel
from sqlalchemy.orm import relationship

class User( UserModel,Base):
    __tablename__ = "users"
    role = relationship("Role", back_populates="users")
    user_privileges = relationship("UserPrivilege", back_populates="user")

class UserPrivilege(UserPrivilegeModel,Base):
    __tablename__ = "user_privileges"
    user = relationship("User", back_populates="user_privileges")
    privilege = relationship("Privilege", back_populates="privilege_users")

metadata= Base.metadata
