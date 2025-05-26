from .auth.models import metadata as user_metadata,Base
from .logger.model import metadata as logger_metadata
from .database import  database
from ..app_one.models import metadata as myapp_metadata
from ..app_two.models import metadata as myapp2_metadata
from ..app_three.models import metadata as myapp3_metadata
from sqlalchemy import MetaData

target_metadata = MetaData()

target_metadata = Base.metadata
target_metadata = user_metadata
target_metadata = logger_metadata
target_metadata = myapp_metadata
target_metadata = myapp2_metadata
target_metadata = myapp3_metadata
database.target_metadata = target_metadata
database.create_tables()
