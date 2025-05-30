
from sqlalchemy import Boolean, Column, ForeignKey, Integer

class UserPrivilegeModel:
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    privilege_id = Column(Integer, ForeignKey("privileges.id"),nullable=False)
    is_active = Column(Boolean, default=True)

