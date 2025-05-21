from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from sqlalchemy.orm import Session, sessionmaker

from fastapi import status


class SessionManager:

    def __init__(
        self, is_async_env: bool, session_maker: sessionmaker[Session]
    ) -> None:
        self.__session_maker: sessionmaker[Session] = session_maker
        self.__is_async_env = is_async_env

    @property
    def is_async_env(self):
        return self.__is_async_env

    @is_async_env.setter
    def is_async_env(self,is_async_env:bool):
        self.__is_async_env=is_async_env

    @property
    def session_maker(self) -> sessionmaker[Session]:
        return self.__session_maker

    @session_maker.setter
    def session_maker(self, session_maker: sessionmaker[Session]) -> None:
        self.__session_maker = session_maker

    def yield_session(self):
        db = self.__session_maker()
        if not db:
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="",
            )
        return db

    def get_sync_db(self):
        db= self.__session_maker()
        try :
            yield db
        except Exception as e:
            detail = f"Cannot yield session , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail,
            )
        finally:
            db.close()

    async def get_async_db(self):
        async with self.__session_maker() as session:
            try :
                yield session
            except Exception as e:
                detail = f"Cannot yield session , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=detail,
                )
