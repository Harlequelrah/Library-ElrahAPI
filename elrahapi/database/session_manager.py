from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from sqlalchemy.orm import Session, sessionmaker
from typing import Any
from fastapi import status
import asyncio
from elrahapi.utility.types import ElrahSession


class SessionManager:

    def __init__(
        self, is_async_env: bool, session_maker: sessionmaker[ElrahSession]
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

    async def rollback_session(self, session: ElrahSession):
        if self.is_async_env:
            await session.rollback()
        else:
            session.rollback()
    async def close_session(self,session:ElrahSession):
        if self.is_async_env:
            await session.close()
        else:
            session.close()

    async def delete_and_commit(self,session: ElrahSession, object: Any):
        if self.is_async_env:
            await session.delete(object)
            await session.commit()
        else:
            session.delete(object)
            session.commit()

    async def commit_and_refresh(self,session:ElrahSession,object:Any):
        if self.is_async_env:
            await session.commit()
            await session.refresh(object)
        else:
            session.commit()
            session.refresh(object)

    async def get_session(self):
        try:
            session = self.__session_maker()
            return session
        except Exception as e:
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while getting session: {str(e)}",
            )

    def get_session_for_script(self):
        try :
            loop=asyncio.get_running_loop()
            return loop.run_until_complete(self.get_session())
        except RuntimeError:
            return asyncio.run(self.get_session())

    async def yield_session(self):
        if self.is_async_env:
            async for session in self.get_async_db():
                try :
                    yield session
                except GeneratorExit:
                    pass
                    # print(f"GeneratorExit caught in yield_session, session will not be closed , session ID: {id(session)}")
        else :
            for session in self.get_sync_db():
                try :
                    yield session
                except GeneratorExit:
                    pass
                    # print(f"GeneratorExit caught in yield_session, session will not be closed , session ID: {id(session)}")

    def get_sync_db(self):
        session= self.__session_maker()
        yield session

    async def get_async_db(self):
        async with self.__session_maker() as session:
            yield session
