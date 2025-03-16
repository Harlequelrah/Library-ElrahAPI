

from typing import Optional


class CrudModels:
    def __init__(self,entity_name:str, primary_key_name:str,SQLAlchemyModel:type,PydanticModel:Optional[type]=None,CreateModel:Optional[type]=None,UpdateModel:Optional[type]=None,PatchModel:Optional[type]=None):
        self.__entity_name = entity_name
        self.__primary_key_name=primary_key_name
        self.__SQLAlchemyModel = SQLAlchemyModel
        self.__PydanticModel = PydanticModel
        self.__CreateModel = CreateModel
        self.__UpdateModel = UpdateModel
        self.__PatchModel = PatchModel


    @property
    def entity_name(self):
        return self.__entity_name

    @property
    def primary_key_name(self)->str:
        return self.__primary_key_name

    @property
    def sqlalchemy_model(self):
        return self.__SQLAlchemyModel

    @property
    def pydantic_model(self):
        return self.__PydanticModel

    @property
    def create_pydantic_model(self):
        return self.__CreateModel

    @property
    def update_pydantic_model(self):
        return self.__UpdateModel

    @property
    def patch_pydantic_model(self):
        return self.__PatchModel


    @entity_name.setter
    def entity_name(self, entity_name: str):
        self.__entity_name = entity_name

    @primary_key_name.setter
    def primary_key_name(self, primary_key_name: str):
        self.__primary_key_name = primary_key_name

    @sqlalchemy_model.setter
    def sqlalchemy_model(self, model):
        self.__SQLAlchemyModel = model

    @pydantic_model.setter
    def pydantic_model(self, model):
        self.__PydanticModel = model

    @create_pydantic_model.setter
    def create_pydantic_model(self, model):
        self.__CreateModel = model

    @update_pydantic_model.setter
    def update_pydantic_model(self, model):
        self.__UpdateModel = model

    @patch_pydantic_model.setter
    def patch_pydantic_model(self, model):
        self.__PatchModel = model





