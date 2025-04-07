from elrahapi.authorization.user_role_model import UserRoleModel
from ..database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Table
from elrahapi.user.model import UserModel
from  elrahapi.authorization.user_privilege_model import UserPrivilegeModel
from sqlalchemy.orm import relationship
from elrahapi.authorization.role_model import RoleModel
from elrahapi.authorization.privilege_model import PrivilegeModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeModel
from elrahapi.authorization.privilege_model import PrivilegeModel


class User( UserModel,Base):
    __tablename__ = "users"
    user_privileges = relationship("UserPrivilege", back_populates="user")
    user_roles=relationship("UserRole",back_populates="user")

class Role(RoleModel,Base):
    __tablename__ = "roles"
    role_privileges = relationship(
        "RolePrivilege",  back_populates="role"
    )
    role_users=relationship(
        "UserRole",back_populates="role"
    )

class RolePrivilege(RolePrivilegeModel,Base):
    __tablename__= 'role_privileges'
    role= relationship("Role",back_populates='role_privileges')
    privilege=relationship("Privilege",back_populates="privilege_roles")

class Privilege(PrivilegeModel,Base):
    __tablename__ = "privileges"
    privilege_roles = relationship(
        "RolePrivilege",  back_populates="privilege"
    )
    privilege_users = relationship("UserPrivilege", back_populates="privilege")


class UserPrivilege(UserPrivilegeModel,Base):
    __tablename__ = "user_privileges"
    user = relationship("User", back_populates="user_privileges")
    privilege = relationship("Privilege", back_populates="privilege_users")

class UserRole(UserRoleModel,Base):
    __tablename__ = "user_roles"
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="role_users")

metadata= Base.metadata
