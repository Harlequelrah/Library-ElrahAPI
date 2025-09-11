from enum import Enum
from typing import TypeAlias


class RelationRoutesName(str, Enum):
    CREATE_RELATION = "create-relation"
    DELETE_RELATION = "delete-relation"
    CREATE_BY_RELATION = "create-by-relation"
    SOFT_DELETE_BY_RELATION = "soft-delete-by-relation"
    DELETE_BY_RELATION = "delete-by-relation"
    UPDATE_BY_RELATION = "update-by-relation"
    PATCH_BY_RELATION = "patch-by-relation"
    READ_ALL_BY_RELATION = "read-all-by-relation"
    READ_ONE_BY_RELATION = "read-one-by-relation"
    READ_ONE_RELATION = "read-one-relation"


class DefaultRoutesName(str, Enum):

    COUNT = "count"
    READ_ALL = "read-all"
    READ_ONE = "read-one"
    READ_ONE_USER = "read-one-user"
    CREATE = "create"
    BULK_CREATE = "bulk-create"
    BULK_DELETE = "bulk-delete"
    BULK_SOFT_DELETE = "bulk-soft-delete"
    UPDATE = "update"
    PATCH = "patch"
    DELETE = "delete"
    SOFT_DELETE = "soft-delete"
    READ_CURRENT_USER = "read-current-user"
    TOKEN_URL = "tokenUrl"
    # GET_REFRESH_TOKEN = "get-refresh-token"
    REFRESH_TOKEN = "refresh-token"
    LOGIN = "login"
    CHANGE_PASSWORD = "change-password"
    CHANGE_USER_STATE = "change-user-state"


CREATE_ALL_PRIVILEGE_ROUTES_NAME: list[DefaultRoutesName] = [
    DefaultRoutesName.CREATE,
    DefaultRoutesName.READ_ALL,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.UPDATE,
    DefaultRoutesName.DELETE,
    DefaultRoutesName.SOFT_DELETE,
    DefaultRoutesName.PATCH,
    DefaultRoutesName.BULK_CREATE,
    DefaultRoutesName.BULK_DELETE,
    DefaultRoutesName.BULK_SOFT_DELETE,
]
RoutesName: TypeAlias = DefaultRoutesName | RelationRoutesName

READ_ROUTES_NAME: list[RoutesName] = [
    DefaultRoutesName.READ_ALL,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.READ_CURRENT_USER,
    DefaultRoutesName.READ_ONE_USER,
    RelationRoutesName.READ_ALL_BY_RELATION,
    RelationRoutesName.READ_ONE_BY_RELATION,
]
DEFAULT_DETAIL_ROUTES_NAME: list[DefaultRoutesName] = [
    DefaultRoutesName.DELETE,
    DefaultRoutesName.UPDATE,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.CHANGE_USER_STATE,
    DefaultRoutesName.PATCH,
    DefaultRoutesName.SOFT_DELETE,
]

DEFAULT_ROUTES_NAME: list[DefaultRoutesName] = [
    DefaultRoutesName.CREATE,
    DefaultRoutesName.READ_ALL,
    DefaultRoutesName.READ_ONE,
    DefaultRoutesName.UPDATE,
    DefaultRoutesName.DELETE,
    DefaultRoutesName.PATCH,
]
