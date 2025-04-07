from typing import List, Optional
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.router_default_routes_name import DEFAULT_DETAIL_ROUTES_NAME, DEFAULT_NO_DETAIL_ROUTES_NAME, DefaultRoutesName


class DEFAULT_ROUTE_CONFIG:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class RouteConfig:


    def __init__(
        self,
        route_name: DefaultRoutesName,
        route_path: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        is_activated: bool = False,
        is_protected: bool = False,
        is_unlocked: Optional[bool] = False,
        roles : Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ):
        self.route_name = route_name
        self.is_activated = is_activated
        self.is_protected = is_protected
        self.route_path = self.validate_route_path(route_name,route_path)
        self.summary = summary
        self.description = description
        self.is_unlocked = is_unlocked
        self.roles = [role.strip().upper() for role in roles if roles] if roles else []
        self.privileges = [auth.strip().upper() for auth in privileges] if privileges else []

    def validate_route_path(self,route_name:str,route_path:Optional[str]=None):
        if route_path : return route_path
        else:
            if route_name in  DEFAULT_DETAIL_ROUTES_NAME or route_name in DEFAULT_NO_DETAIL_ROUTES_NAME:
                return ""
            else : return f"/{route_name.value}"


    def get_authorizations(self,authentication:AuthenticationManager)-> List[callable]:
        return authentication.check_authorizations(
            roles_name = self.roles,
            privieles_name=self.privileges
        )


class AuthorizationConfig:
    def __init__(self, route_name:DefaultRoutesName, roles: Optional[List[str]] = None, privileges: Optional[List[str]] = None):
        self.route_name = route_name
        self.roles = roles if roles else []
        self.privileges = privileges if privileges else []


