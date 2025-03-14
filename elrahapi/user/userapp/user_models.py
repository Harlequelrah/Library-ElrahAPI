from myproject.settings.database import Base, authentication
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from elrahapi.user.models import UserModel
from  elrahapi.authorization.user_privilege_model import UserPrivilegeModel
from sqlalchemy.orm import relationship
from elrahapi.authorization.privilege_model import PrivilegeModel


# class Privilege(PrivilegeModel,Base):
#     __tablename__ = "privileges"
#     privilege_roles = relationship(
#         "RolePrivilege",  back_populates="privilege"
#     )
#     privilege_users = relationship("UserPrivilege", back_populates="privilege")


# class Role(RoleModel,Base):
#     __tablename__ = "roles"
#     users = relationship("User", back_populates="role")
#     role_privileges = relationship(
#         "RolePrivilege",  back_populates="role"
#     )

# class RolePrivilege(RolePrivilegeModel,Base):
#     __tablename__= 'role_privileges'
#     role= relationship("Role",back_populates='role_privileges')
#     privilege=relationship("Privilege",back_populates="privilege_roles")


class User( UserModel,Base):
    __tablename__ = "users"
    role = relationship("Role", back_populates="users")
    user_privileges = relationship("UserPrivilege", back_populates="user")


class UserPrivilege(UserPrivilegeModel,Base):
    __tablename__ = "user_privileges"
    user = relationship("User", back_populates="user_privileges")
    privilege = relationship("Privilege", back_populates="privilege_users")





authentication.User = User
metadata= Base.metadata
