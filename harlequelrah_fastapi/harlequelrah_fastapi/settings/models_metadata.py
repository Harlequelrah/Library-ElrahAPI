# from todolistapp import model
from sqlalchemy import MetaData
# from userapp import user_model
from harlequelrah_fastapi.middleware.logapp import log_model


target_metadata = MetaData()
# target_metadata = model.Base.metadata
# target_metadata = logger_model.Base.metadata
# target_metadata = user_model.Base.metadata
