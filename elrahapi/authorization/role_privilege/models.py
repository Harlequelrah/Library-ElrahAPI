from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean

from elrahapi.utility.models import AdditionalModelFields
from sqlalchemy.orm import validates
from sqlalchemy.sql import func


class RolePrivilegeModel(AdditionalModelFields):
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    privilege_id = Column(Integer, ForeignKey("privileges.id"), nullable=False)
    # begin_date = Column(DateTime, nullable=True)
    # end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # @validates("is_active")
    # def validate_is_active(self, key, value):
    #     if (
    #         self.begin_date
    #         and self.end_date
    #         and func.now() < self.begin_date
    #         and func.now() > self.end_date
    #     ):
    #         return False
