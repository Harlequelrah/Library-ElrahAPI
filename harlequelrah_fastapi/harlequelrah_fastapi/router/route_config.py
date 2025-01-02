from typing import List, Optional


class DEFAULT_ROUTES_CONFIG:
    def __init__(self, route_name: str, summary: str, description: str):
        self.route_name = route_name
        self.summary = summary
        self.description = description


class RouteConfig:

    DEFAULT_ROUTES_NAME: List[DEFAULT_ROUTES_CONFIG] = [
        DEFAULT_ROUTES_CONFIG(
            "count", "Get count of entities", "Retrieve the total count of entities"
        ),
        DEFAULT_ROUTES_CONFIG(
            "read-one", "Get one entity", "Retrieve one entity by id"
        ),
        DEFAULT_ROUTES_CONFIG("read-all", "Get all entities", "Retrieve all entities"),
        DEFAULT_ROUTES_CONFIG(
            "read-all-by-filter",
            "Get all entities by filter",
            "Retrieve entities by filter",
        ),
        DEFAULT_ROUTES_CONFIG(
            "create", "Create an entity", "Allow to create an entity"
        ),
        DEFAULT_ROUTES_CONFIG(
            "update", "Update an entity", "Allow to update an entity"
        ),
        DEFAULT_ROUTES_CONFIG("delete", "Delete an entity", "Allow to delete an entity"),
    ]
    DEFAULT_DETAIL_ROUTES=[
        'delete',
        'update',
        'read-one'
    ]

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
        self.route_path = route_path if route_path else  f"/{route_name}/{{id}}" if route_name in self.DEFAULT_DETAIL_ROUTES  else f"/{route_name}"
        self.summary = summary
        self.description = description
        self.is_unlocked = is_unlocked




