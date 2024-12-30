from fastapi_gestschool.myapp import metadata as myapp_metadata
from fastapi_gestschool.myapp2 import metadata as myapp_metadata2
from sqlalchemy import MetaData

target_metadata = MetaData()

# target_metadata = Base.metadata
target_metadata = myapp_metadata
target_metadata = myapp2_metadata
