from app.settings.database.base import Base
from elrahapi.authorization.privilege.models import PrivilegeModel
from elrahapi.authorization.role.models import RoleModel
from elrahapi.authorization.role_privilege.models import RolePrivilegeModel
from elrahapi.authorization.user_privilege.models import UserPrivilegeModel
from elrahapi.authorization.user_role.models import UserRoleModel
from elrahapi.user.model import UserModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, relationship


class User(UserModel, Base):
    __tablename__ = "users"
    user_privileges: Mapped[list["UserPrivilege"]] = relationship(back_populates="user")
    user_roles: Mapped[list["UserRole"]] = relationship(back_populates="user")
    # user_logs = relationship(LogModel, back_populates="user")


class Role(RoleModel, Base):
    __tablename__ = "roles"
    role_privileges: Mapped[list["RolePrivilege"]] = relationship(
        "RolePrivilege", back_populates="role"
    )
    role_users: Mapped[list["UserRole"]] = relationship(
        "UserRole", back_populates="role"
    )


class RolePrivilege(RolePrivilegeModel, Base):
    __tablename__ = "role_privileges"
    role: Mapped["Role"] = relationship(back_populates="role_privileges")
    privilege: Mapped["Privilege"] = relationship(back_populates="privilege_roles")


class Privilege(PrivilegeModel, Base):
    __tablename__ = "privileges"
    privilege_roles: Mapped[list["RolePrivilege"]] = relationship(
        back_populates="privilege"
    )
    privilege_users: Mapped[list["UserPrivilege"]] = relationship(
        back_populates="privilege"
    )


class UserPrivilege(UserPrivilegeModel, Base):
    __tablename__ = "user_privileges"
    user: Mapped["User"] = relationship(back_populates="user_privileges")
    privilege: Mapped["Privilege"] = relationship(back_populates="privilege_users")


class UserRole(UserRoleModel, Base):
    __tablename__ = "user_roles"
    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="role_users")
