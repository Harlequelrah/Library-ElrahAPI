# from .myapp1.models import base as myapp_base1
# from .myapp2.models import base as myapp_base2
from settings.database import database
from .auth.models import base as auth_base
from .logger.model import base as logger_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

bases: list[DeclarativeMeta] = [auth_base, logger_base]
target_metadata = database.create_target_metadata(bases=bases)
