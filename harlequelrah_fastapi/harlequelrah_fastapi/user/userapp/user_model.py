from my_project.settings.database import Base, authentication
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from harlequelrah_fastapi.exception.auth_exception import INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION
from harlequelrah_fastapi.user.models import UserModel,UserPrivilegeModel
from sqlalchemy.orm import relationship
from harlequelrah_fastapi.authorization.role_model import RoleModel
from harlequelrah_fastapi.authorization.privilege_model import PrivilegeModel


class Privilege(PrivilegeModel,Base):
    __tablename__ = "privileges"
    roles = relationship(
        "Role", secondary="role_privileges", back_populates="privileges"
    )
    privilege_users = relationship("UserPrivilege", back_populates="privilege")


class Role(RoleModel,Base):
    __tablename__ = "roles"
    users = relationship("User", back_populates="role")
    privileges = relationship(
        "Privilege", secondary="role_privileges", back_populates="roles"
    )


role_privileges = Table(
    "role_privileges",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("privilege_id", Integer, ForeignKey("privileges.id")),
)

class User( UserModel,Base):
    __tablename__ = "users"
    role = relationship("Role", back_populates="users")
    user_privileges = relationship("UserPrivilege", back_populates="user")
class UserPrivilege(UserPrivilegeModel,Base):
    __tablename__ = "user_privileges"
    user = relationship("User", back_populates="user_privileges",lazy="joined")
    privilege = relationship("Privilege", back_populates="privilege_users",lazy="joined")





authentication.User = User
metadata= Base.metadata
