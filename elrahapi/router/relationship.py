from typing import Type

from elrahapi.crud.crud_models import CrudModels


class Relationship:

    def __init__(
        self,
        relationship_name: str,
        relationship_crud_models: CrudModels,
        joined_entity_crud_models: CrudModels,
        relationship_key1_name: str,
        relationship_key2_name: str,
        joined_model_key_name: str,
    ):
        self.relationship_name = relationship_name
        self.relationship_crud_models = relationship_crud_models
        self.joined_entity_crud_models = joined_entity_crud_models
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.joined_model_key_name = joined_model_key_name

    async def get_relationship_key1(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key1_name)

    async def get_relationship_key2(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key2_name)

    async def get_joined_model_key(self):
        return await self.joined_entity_crud_models.get_attr(self.joined_model_key_name)
