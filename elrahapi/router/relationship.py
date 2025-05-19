from typing import Type,Optional

from elrahapi.crud.crud_models import CrudModels
from elrahapi.router.route_config import RouteConfig,ResponseModelConfig,AuthorizationConfig
from elrahapi.router.router_default_routes_name import DefaultRoutesName

class RelationRouteConfig:
    def __init__(self,response_model_config:ResponseModelConfig,authorization_config:AuthorizationConfig,route_config:Optional[RouteConfig]=None):
        pass

class Relationship:

    def __init__(
        self,
        relationship_name: str,
        relationship_crud_models: CrudModels,
        joined_entity_crud_models: CrudModels,
        relationship_key1_name: str,
        relationship_key2_name: str,
        joined_model_key_name: str,
        read_all_relations_route_config:Optional[RelationRouteConfig]=None,
        create_relation_route_config:Optional[RelationRouteConfig]=None,
        delete_relation_route_config:Optional[RelationRouteConfig]=None,
    ):
        self.relationship_name = relationship_name
        self.relationship_crud_models = relationship_crud_models
        self.joined_entity_crud_models = joined_entity_crud_models
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.joined_model_key_name = joined_model_key_name
        self.read_all_relations_route_config,self.create_relation_route_config,self.delete_relation_route_config=self.init_routes_configs(read_all_relations_route_config,create_relation_route_config,delete_relation_route_config)

    def init_routes_configs(
        self,
        read_all_relations_route_config:Optional[RouteConfig]=None,
        create_relation_route_config:Optional[RouteConfig]=None,
        delete_relation_route_config:Optional[RouteConfig]=None
    ):
        r1:Optional[RouteConfig]=None
        r2:Optional[RouteConfig]=None
        r3:Optional[RouteConfig]=None
        rel_entity_name=self.joined_entity_crud_models.entity_name
        if read_all_relations_route_config:
            r1=read_all_relations_route_config
        else :
            r1=RouteConfig(
                route_name=DefaultRoutesName.RELATION,
                route_path=f"{{pk1}}/{rel_entity_name}s/{{pk2}}",
                summary=f"Retrive all {rel_entity_name}s",
                description=f"Allow to retrive all {rel_entity_name}s from the relation",
                is_activated=True
            )


    async def get_relationship_key1(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key1_name)

    async def get_relationship_key2(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key2_name)

    async def get_joined_model_key(self):
        return await self.joined_entity_crud_models.get_attr(self.joined_model_key_name)
