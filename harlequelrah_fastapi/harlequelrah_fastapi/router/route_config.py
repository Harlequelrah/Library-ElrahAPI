from typing import List, Optional

from fastapi import Depends

from harlequelrah_fastapi.authentication.authenticate import Authentication
from harlequelrah_fastapi.router.router_default_routes_name import DEFAULT_DETAIL_ROUTES_NAME






class DEFAULT_ROUTE_CONFIG:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class RouteConfig:


    def __init__(
        self,
        route_name: str,
        route_path: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        is_activated: bool = False,
        is_protected: bool = False,
        is_unlocked: Optional[bool] = False,
        roles : Optional[List[str]] = [],
        privileges: Optional[List[str]] =[],
    ):
        self.route_name = route_name
        self.is_activated = is_activated
        self.is_protected = is_protected
        self.route_path = (
            route_path
            if route_path
            else (
                f"/{route_name}/{{id}}"
                if next(
                    (
                        True
                        for default_detail_route_name in DEFAULT_DETAIL_ROUTES_NAME
                        if route_name == default_detail_route_name.value
                    ),
                    False,
                )
                else f"/{route_name}"
            )
        )
        self.summary = summary
        self.description = description
        self.is_unlocked = is_unlocked
        self.roles = [role.strip().upper() for role in roles if roles]
        self.privileges = [auth.strip.upper() for auth in privileges] if privileges else []

    def get_authorizations(self,authentication:Authentication)-> List[callable]:
        authorizations = []
        role_authorization = authentication.check_authorization(roles_name=self.roles)
        authorizations.append(role_authorization)
        for privilege in self.privileges :
            privilege_authorization = authentication.check_authorization(privilege_name=privilege)
            authorizations.append(privilege_authorization)
        return authorizations





