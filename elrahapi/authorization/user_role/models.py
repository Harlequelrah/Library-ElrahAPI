from sqlalchemy import Boolean, Column, ForeignKey, Integer

class UserRoleModel:
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"),nullable=False)
    is_active = Column(Boolean, default=True)

