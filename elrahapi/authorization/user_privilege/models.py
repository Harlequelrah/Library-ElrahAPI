
from pydantic import BaseModel,Field
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel

from elrahapi.user.schemas import UserBaseModel



class UserPrivilegeModel:
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    privilege_id = Column(Integer, ForeignKey("privileges.id"),nullable=False)
    is_active = Column(Boolean, default=True)

