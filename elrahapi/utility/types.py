from typing import TypeAlias

from elrahapi.authentication.token import (
    AccessToken,
    FullTempToken,
    RefreshToken,
    TempToken,
    Token,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

ElrahSession: TypeAlias = Session | AsyncSession
ElrahToken: TypeAlias = AccessToken | RefreshToken | FullTempToken | TempToken | Token
