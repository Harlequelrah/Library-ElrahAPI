from elrahapi.router.relationship import Relationship
from elrahapi.router.router_namespace import (
    RELATION_RULES,
    RelationRoutesName,
    TypeRelation,
)
from elrahapi.router.router_provider import CustomRouterProvider
from elrahapi.router.router_routes_name import DefaultRoutesName
from ..database import session_manager
from ...app_one.cruds import myapp_crud as profile_crud
from ...app_two.cruds import myapp_crud as post_crud
from .configs import authentication
from .cruds import (
    privilege_crud,
    role_crud,
    role_privilege_crud,
    user_crud,
    user_privilege_crud,
    user_role_crud,
)

user_role_relation: Relationship = Relationship(
    relationship_name="user_roles",
    second_entity_crud=role_crud,
    relationship_crud=user_role_crud,
    type_relation=TypeRelation.MANY_TO_MANY_CLASS,
    relationship_key1_name="user_id",
    relationship_key2_name="role_id",
    default_public_relation_routes_name=[
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.DELETE_RELATION,
    ],
)
profile_relation: Relationship = Relationship(
    relationship_name="profile",
    second_entity_crud=profile_crud,
    type_relation=TypeRelation.ONE_TO_ONE,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.ONE_TO_ONE],
)
post_relation: Relationship = Relationship(
    relationship_name="posts",
    second_entity_crud=post_crud,
    second_entity_fk_name="user_id",
    type_relation=TypeRelation.ONE_TO_MANY,
    default_public_relation_routes_name=RELATION_RULES[TypeRelation.ONE_TO_MANY],
)
user_router_provider = CustomRouterProvider(
    prefix="/users",
    tags=["users"],
    crud=user_crud,
    authentication=authentication,
    read_with_relations=True,
    session_manager=session_manager,
    relations=[
        post_relation
        # user_role_relation,
        # profile_relation
    ],
)


user_privilege_router_provider = CustomRouterProvider(
    prefix="/users/privileges",
    tags=["user_privileges"],
    crud=user_privilege_crud,
    authentication=authentication,
    session_manager=session_manager,
)

role_router_provider = CustomRouterProvider(
    prefix="/roles",
    tags=["roles"],
    crud=role_crud,
    authentication=authentication,
    session_manager=session_manager,
)

privilege_router_provider = CustomRouterProvider(
    prefix="/privileges",
    tags=["privileges"],
    crud=privilege_crud,
    authentication=authentication,
    session_manager=session_manager,
    privileges=["CAN_ADD_PRIVILEGE"],
)

role_privilege_router_provider = CustomRouterProvider(
    prefix="/roles/privileges",
    tags=["role_privileges"],
    crud=role_privilege_crud,
    authentication=authentication,
    session_manager=session_manager,
)

user_role_router_provider = CustomRouterProvider(
    prefix="/users/roles",
    tags=["user_roles"],
    crud=user_role_crud,
    authentication=authentication,
    session_manager=session_manager,
)


# user_router = user_router_provider.get_protected_router()
user_router = user_router_provider.get_mixed_router(
    public_routes_name=[DefaultRoutesName.CREATE],
    protected_routes_name=[
        DefaultRoutesName.DELETE,
        DefaultRoutesName.UPDATE,
        DefaultRoutesName.PATCH,
        DefaultRoutesName.READ_ALL,
        DefaultRoutesName.READ_ONE,
    ],
)

user_privilege_router = user_privilege_router_provider.get_protected_router()
user_role_router = user_role_router_provider.get_protected_router()
role_router = role_router_provider.get_protected_router()
privilege_router = privilege_router_provider.get_protected_router()
role_privilege_router = role_privilege_router_provider.get_protected_router()
