from sqlalchemy.orm import sessionmaker, Session
from fastapi import status
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
class SessionManager :

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.__session_factory: sessionmaker[Session]=session_factory

    @property
    def session_factory(self) -> sessionmaker[Session]:
        return self.__session_factory

    @session_factory.setter
    def session_factory(self, session_factory: sessionmaker[Session]) -> None:
        self.__session_factory = session_factory

    def yield_session(self):
        db = self.__session_factory()
        if not db:
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cannot yield session",
            )
        return db
