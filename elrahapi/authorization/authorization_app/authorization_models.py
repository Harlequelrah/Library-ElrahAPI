from sqlalchemy.orm import relationship
from elrahapi.authorization.role_model import RoleModel
from elrahapi.authorization.privilege_model import PrivilegeModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeModel
from myproject.settings.database import Base
from elrahapi.authorization.privilege_model import PrivilegeModel


class Role(RoleModel,Base):
    __tablename__ = "roles"
    users = relationship("User", back_populates="role")
    # admins = relationship("Admin", back_populates="role")
    role_privileges = relationship(
        "RolePrivilege",  back_populates="role"
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
    # privilege_admins = relationship("AdminPrivilege", back_populates="privilege")


metadata= Base.metadata
