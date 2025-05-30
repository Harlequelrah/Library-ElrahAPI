from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeAlias

ElrahSession : TypeAlias = Session|AsyncSession


