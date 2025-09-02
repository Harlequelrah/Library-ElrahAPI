# from pydantic import BaseModel, Field
# from datetime import datetime
# from decimal import Decimal

# # from .meta_models import EntityBaseModel

# class EntityCreateModel(BaseModel):
#     pass

# class EntityUpdateModel(BaseModel):
#     pass

# class EntityPatchModel(BaseModel):
#     pass

# class EntityReadModel():
#     id : int
#     date_created: datetime
#     date_updated: datetime
#     date_deleted: datetime | None = None
#     is_deleted:bool
#     config_model=ConfigDict(from_attributes=True)


# class EntityFullReadModel(EntityReadModel):
    # config_model=ConfigDict(from_attributes=True)
