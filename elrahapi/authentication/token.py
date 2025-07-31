from pydantic import BaseModel
from enum import Enum
class AccessToken(BaseModel):
    access_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TempToken(BaseModel):
    temp_token: str
    token_type:str

class FullTempToken(TempToken):
    status:str
    message:str

class TokenType(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    TEMP_TOKEN = "temp_token"
