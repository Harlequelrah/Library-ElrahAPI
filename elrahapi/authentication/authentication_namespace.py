

from fastapi.security import OAuth2PasswordBearer

TOKEN_URL = "auth/tokenUrl"
OAUTH2_SCHEME = OAuth2PasswordBearer(TOKEN_URL)
REFRESH_TOKEN_EXPIRATION = 86400000
ACCESS_TOKEN_EXPIRATION = 3600000

