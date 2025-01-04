from typing import List,Optional
from harlequelrah_fastapi.router.route_config import DEFAULT_ROUTE_CONFIG, RouteConfig
from harlequelrah_fastapi.router.router_namespace import DEFAULT_ROUTES_CONFIGS, DEFAULTROUTESNAME


def exclude_route(
    routes: List[RouteConfig],
    exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
):
    init_data: List[RouteConfig] = []
    if exclude_routes_name:
        for route in routes:
            if route.route_name not in [route_name.value for route_name in exclude_routes_name]:
                init_data.append(route)
    return init_data if init_data else routes


def get_single_route(route_name:DEFAULTROUTESNAME , type_route : Optional[str] = None)->RouteConfig:
    config : DEFAULT_ROUTE_CONFIG = DEFAULT_ROUTES_CONFIGS[route_name]
    return RouteConfig(
        route_name=route_name.value,
        is_activated=True,
        summary=config.summary,
        description=config.description,
        is_protected= type_route == "protected"
        )
