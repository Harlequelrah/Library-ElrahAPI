from typing import List, Optional



class DEFAULT_ROUTE_CONFIG:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class RouteConfig:
    DEFAULT_DETAIL_ROUTES_NAME = ["delete", "update", "read-one"]

    def __init__(
        self,
        route_name: str,
        route_path: Optional[str]=None,
        summary: Optional[str]=None,
        description: Optional[str]=None,
        is_activated: bool = False,
        is_protected: bool = False,
        is_unlocked: Optional[bool] = False,
    ):
        self.route_name = route_name
        self.is_activated = is_activated
        self.is_protected = is_protected
        self.route_path = route_path if route_path else  f"/{route_name}/{{id}}" if route_name in self.DEFAULT_DETAIL_ROUTES_NAME  else f"/{route_name}"
        self.summary = summary
        self.description = description
        self.is_unlocked = is_unlocked
