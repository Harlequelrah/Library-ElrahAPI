from sqlalchemy import Column, ForeignKey, Integer
from harlequelrah_fastapi.authorization.role.role_model import RoleModel
from harlequelrah_fastapi.authorization.privilege.privilege_model import PrivilegeModel
from sqlalchemy.orm import relationship
class Privilege(PrivilegeModel):
    __tablename__ = "privileges"
    roles = relationship("Privilege", back_populates="role")

class Role(RoleModel):
    __tablename__ = "roles"
    role = relationship("Role", back_populates="privileges")
    role_id = Column(Integer, ForeignKey("roles.id"))
