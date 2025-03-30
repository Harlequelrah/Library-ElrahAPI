from .database import Base
from .auth.models import metadata as user_metadata
from .logger.model import metadata as logger_metadata
# from ..myapp.models import metadata as myapp_metadata
# from ..myapp2.models import metadata as myapp2_metadata
from sqlalchemy import MetaData

target_metadata = MetaData()

target_metadata = Base.metadata
target_metadata = user_metadata
target_metadata = logger_metadata
# target_metadata = myapp_metadata
# target_metadata = myapp2_metadata
