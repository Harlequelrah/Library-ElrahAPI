from sqlalchemy import Boolean, Column, ForeignKey, Integer

from elrahapi.utility.models import AdditionalModelFields


class UserPrivilegeModel(AdditionalModelFields):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    privilege_id = Column(Integer, ForeignKey("privileges.id"),nullable=False)
    is_active = Column(Boolean, default=True)
