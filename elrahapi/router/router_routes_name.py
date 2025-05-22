from enum import Enum


class RelationRoutesName(str,Enum):
    CREATE_RELATION="create-relation"
    DELETE_RELATION="delete-relation"
    CREATE_BY_RELATION="create-by-relation"
    DELETE_BY_RELATION="delete-by-relation"
    UPDATE_BY_RELATION="update-by-relation"
    PATCH_BY_RELATION="patch-by-relation"
    READ_ALL_BY_RELATION="read-all-by-relation"
    READ_ONE_BY_RELATION="read-one-by-relation"


class DefaultRoutesName(str, Enum):

    COUNT = "count"
    READ_ALL = "read-all"
    READ_ONE = "read-one"
    READ_ONE_USER = "read-one-user"
    CREATE = "create"
    BULK_CREATE = "bulk-create"
    BULK_DELETE = "bulk-delete"
    UPDATE = "update"
    PATCH = "patch"
    DELETE = "delete"
    READ_CURRENT_USER = "read-current-user"
    TOKEN_URL = "tokenUrl"
    GET_REFRESH_TOKEN = "get-refresh-token"
    REFRESH_TOKEN = "refresh-token"
    LOGIN = "login"
    CHANGE_PASSWORD = "change-password"
    CHANGE_USER_STATE = "change-user-state"

DEFAULT_DETAIL_ROUTES_NAME = [
    DefaultRoutesName.DELETE,
    DefaultRoutesName.UPDATE,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.CHANGE_USER_STATE,
    DefaultRoutesName.PATCH,
]

DEFAULT_NO_DETAIL_ROUTES_NAME = [
    DefaultRoutesName.READ_ALL,
    DefaultRoutesName.CREATE,
    ]
    
