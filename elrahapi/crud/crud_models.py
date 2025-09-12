from typing import Type
from fastapi import status
from pydantic import BaseModel
from elrahapi.exception.exceptions_utils import raise_custom_http_exception


class CrudModels:
    def __init__(
        self,
        entity_name: str,
        primary_key_name: str,
        SQLAlchemyModel: Type,
        ReadModel: Type[BaseModel],
        CreateModel: Type[BaseModel] | None = None,
        UpdateModel: Type[BaseModel] | None = None,
        PatchModel: Type[BaseModel] | None = None,
        FullReadModel: Type[BaseModel] | None = None,
    ):
        self.__entity_name = entity_name
        self.__primary_key_name = primary_key_name
        self.__SQLAlchemyModel = SQLAlchemyModel
        self.__ReadModel = ReadModel
        self.__CreateModel = CreateModel
        self.__UpdateModel = UpdateModel
        self.__PatchModel = PatchModel
        self.__FullReadModel = FullReadModel

    @property
    def entity_name(self):
        return self.__entity_name

    @property
    def primary_key_name(self) -> str:
        return self.__primary_key_name

    @property
    def sqlalchemy_model(self):
        return self.__SQLAlchemyModel

    @property
    def read_model(self):
        return self.__ReadModel

    @property
    def full_read_model(self):
        return self.__FullReadModel

    @property
    def create_model(self):
        return self.__CreateModel

    @property
    def update_model(self):
        return self.__UpdateModel

    @property
    def patch_model(self):
        return self.__PatchModel

    @entity_name.setter
    def entity_name(self, entity_name: str):
        self.__entity_name = entity_name

    @primary_key_name.setter
    def primary_key_name(self, primary_key_name: str):
        self.__primary_key_name = primary_key_name

    @sqlalchemy_model.setter
    def sqlalchemy_model(self, model: Type[BaseModel]):
        self.__SQLAlchemyModel = model

    @read_model.setter
    def read_model(self, model: Type[BaseModel]):
        self.__ReadModel = model

    @full_read_model.setter
    def full_read_model(self, model: Type[BaseModel]):
        self.__FullReadModel = model

    @create_model.setter
    def create_model(self, model: Type[BaseModel]):
        self.__CreateModel = model

    @update_model.setter
    def update_model(self, model: Type[BaseModel]):
        self.__UpdateModel = model

    @patch_model.setter
    def patch_model(self, model: Type[BaseModel]):
        self.__PatchModel = model

    def get_pk(self):
        return self.get_attr(self.__primary_key_name)

    def get_attr(self, attr_name: str):
        try:
            return getattr(self.__SQLAlchemyModel, attr_name)
        except Exception as e:
            detail = f"Error occurred while getting attribute {attr_name} for entity {self.entity_name} , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )
