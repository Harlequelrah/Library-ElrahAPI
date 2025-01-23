from enum import Enum

class DefaultRoutesName(str, Enum):
    COUNT = "count"
    READ_ALL_BY_FILTER = "read-all-by-filter"
    READ_ALL = "read-all"
    READ_ONE = "read-one"
    READ_ONE_USER = "read-one-user"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ_CURRENT_USER = "read-current-user"
    TOKEN_URL = "tokenUrl"
    GET_REFRESH_TOKEN = "get-refresh-token"
    REFRESH_TOKEN = "refresh-token"
    LOGIN = "login"
    CHANGE_PASSWORD = "change-password"

DEFAULT_DETAIL_ROUTES_NAME = [
    DefaultRoutesName.DELETE,
    DefaultRoutesName.UPDATE,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.READ_ONE_USER,
]
