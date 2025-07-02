# from .myapp1.models import metadata as myapp_metadata1
# from .myapp2.models import metadata as myapp_metadata2
from .auth.models import metadata as auth_metadata,database
from .logger.model import metadata as logger_metadata
from sqlalchemy import MetaData
target_metadata = MetaData()
# target_metadata = myapp_metadata1
# target_metadata = myapp_metadata2
target_metadata = auth_metadata
target_metadata = logger_metadata
