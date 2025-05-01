from typing import  Type

from elrahapi.crud.crud_models import CrudModels

class ModelRelation:

    def __init__(
        self,
        relationship_name: str,
        relationship_crud_models: CrudModels,
        result_crud_models: CrudModels,
        relationship_key1_name: str,
        relationship_key2_name: str,
        result_model_key_name: str,
    ):
        self.relationship_name = relationship_name
        self.relationship_crud_models = relationship_crud_models
        self.result_crud_models = result_crud_models
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.result_model_key_name = result_model_key_name

    async def get_relationship_key1(self):
        return self.relationship_crud_models.get_attr(self.relationship_key1_name)

    async def get_relationship_key2(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key2_name)


    async def get_result_model_key(self):
        return await self.result_crud_models.get_attr(self.result_model_key_name)
