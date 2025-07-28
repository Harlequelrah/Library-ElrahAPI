from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.database.session_manager import SessionManager
from elrahapi.websocket.connection_manager import ConnectionManager

class MiddlewareHelper:
    def __init__(
        self,
        LogModel=None,
        session_manager: SessionManager | None = None,
        websocket_manager: ConnectionManager | None = None,
        authentication: AuthenticationManager | None = None,
    ):
        self.LogModel = LogModel
        self.session_manager = session_manager
        self.websocket_manager = websocket_manager
        self.authentication = authentication
        self.session_manager=authentication.session_manager if authentication else session_manager
