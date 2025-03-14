

class CrudModels:
    def __init__(self,SQLAlchemyModel:type,PydanticModel:type,CreateModel:type,UpdateModel:type,PatchModel:type):
        self.__SQLAlchemyModel = SQLAlchemyModel
        self.__PydanticModel = PydanticModel
        self.__CreateModel = CreateModel
        self.__UpdateModel = UpdateModel
        self.__PatchModel = PatchModel


    @property
    def sqlalchemy_model(self):
        return self.__SQLAlchemyModel

    @property
    def pydantic_model(self):
        return self.__PydanticModel

    @property
    def create_model(self):
        return self.__CreateModel

    @property
    def update_model(self):
        return self.__UpdateModel

    @property
    def patch_model(self):
        return self.__PatchModel

    @sqlalchemy_model.setter
    def sqlalchemy_model(self, model):
        self.__SQLAlchemyModel = model

    @pydantic_model.setter
    def pydantic_model(self, model):
        self.__PydanticModel = model

    @create_model.setter
    def create_model(self, model):
        self.__CreateModel = model

    @update_model.setter
    def update_model(self, model):
        self.__UpdateModel = model

    @patch_model.setter
    def patch_model(self, model):
        self.__PatchModel = model





