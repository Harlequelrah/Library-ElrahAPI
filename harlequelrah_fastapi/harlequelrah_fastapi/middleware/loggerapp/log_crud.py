from harlequelrah_fastapi.middleware.logCrud import LogCrud
from settings.secret import authentication
from log_model import Logger


logCrud= LogCrud(session_factory=authentication.session_factory,LoggerModel=Logger)
