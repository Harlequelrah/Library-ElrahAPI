# from pydantic import BaseModel, ConfigDict, Field

# from datetime import datetime
# from decimal import Decimal

# # from .meta_models import EntityBaseModel

# class EntityCreateModel(BaseModel):
#     pass

# class EntityUpdateModel(BaseModel):
#     pass

# class EntityPatchModel(BaseModel):
#     pass

# class EntityReadModel(EntityBaseModel):
#     id : int
#     date_created: datetime
#     date_updated: datetime
#     date_deleted: datetime | None = None
#     is_deleted:bool
#     model_config=ConfigDict(from_attributes=True)


# class EntityFullReadModel(EntityReadModel):
#     model_config=ConfigDict(from_attributes=True)
