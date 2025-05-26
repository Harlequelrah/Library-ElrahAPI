from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, sessionmaker

from fastapi import status

from elrahapi.utility.types import ElrahSession


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

    async def close_session(self,session:ElrahSession):
        if self.is_async_env:
            await session.close()
        else:
            session.close()

    async def get_session(self):
        if self.is_async_env:
            return anext(self.get_async_db())
        else:
            return next(self.get_sync_db())

    async def yield_session(self):
        try :
            if self.is_async_env:
                return  self.get_async_db()
                # return await anext(db)

            else :
                return  self.get_sync_db()
                # return next(db)

        except Exception as e:
            detail = f"Cannot yield session , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail,
            )

    def get_sync_db(self):
        db= self.__session_maker()
        try :
            yield db
        finally:
            db.close()

    async def get_async_db(self):
        async with self.__session_maker() as session:
            yield session
