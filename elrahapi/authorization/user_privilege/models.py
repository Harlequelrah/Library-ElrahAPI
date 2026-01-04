from elrahapi.utility.models import AdditionalModelFields
from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


class UserPrivilegeModel(AdditionalModelFields):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    privilege_id: Mapped[int] = mapped_column(ForeignKey("privileges.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
