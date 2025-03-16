
from elrahapi.router.router_provider import CustomRouterProvider
from .authorization_cruds import roleCrud,privilegeCrud,rolePrivilegeCrud

role_router_provider = CustomRouterProvider(
    prefix="/roles",
    tags=["roles"],
    crud=roleCrud,
)

privilege_router_provider = CustomRouterProvider(
    prefix="/privileges",
    tags=["privileges"],
    crud=privilegeCrud,
)



role_privilege_router_provider=CustomRouterProvider(
    prefix='/roles/privileges',
    tags=["roles_privileges"],
    crud=rolePrivilegeCrud
)
