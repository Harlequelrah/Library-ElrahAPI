from elrahapi.database.session_manager import SessionManager
from sqlalchemy import create_engine, text , MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from typing import  Optional
import asyncio
class DatabaseManager:

    def __init__(
        self,
        database: str,
        database_username: str,
        database_password: str,
        database_connector: str,
        database_name: str,
        database_server: str,
        database_async_connector: str,
        is_async_env=bool
    ):
        self.__database = database
        self.__database_username = database_username
        self.__database_password = database_password
        self.__database_connector = database_connector
        self.__database_async_connector = database_async_connector
        self.database_name = database_name
        self.__database_server = database_server
        self.__base:Optional[DeclarativeMeta]=None
        self.__target_metadata:MetaData= MetaData()
        self.__session_manager:SessionManager=None
        self.__is_async_env= True if is_async_env is True and self.__database_async_connector  else False


    @property
    def session_manager(self):
        return self.__session_manager
    @session_manager.setter
    def session_manager(self,session_manager:SessionManager):
        self.__session_manager=session_manager
    @property
    def target_metadata(self):
        return self.__target_metadata

    @target_metadata.setter
    def target_metadata(self,target_metadata:MetaData):
        self.__target_metadata=target_metadata

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self,base:DeclarativeMeta):
        self.__base=base

    @property
    def database_username(self):
        return self.__database_username

    @database_username.setter
    def database_username(self, database_username: str):
        self.__database_username = database_username

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database: str):
        self.__database = database

    @property
    def database_async_connector(self):
        return self.__database_async_connector

    @database_async_connector.setter
    def database_async_connector(self, database_async_connector: str):
        self.__database_async_connector = database_async_connector

    @property
    def database_password(self):
        return self.__database_password

    @database_password.setter
    def database_password(self, database_password: str):
        self.__database_password = database_password

    @property
    def database_connector(self):
        return self.__database_connector

    @database_connector.setter
    def database_connector(self, database_connector: str):
        self.__database_connector = database_connector

    @property
    def database_name(self):
        return self.__database_name

    @database_name.setter
    def database_name(self, database_name: str):
        if self.database == "sqlite" and database_name :
            self.__database_name = "database"
        else:
            self.__database_name = database_name

    @property
    def database_server(self):
        return self.__database_server

    @database_server.setter
    def database_server(self, database_server: str):
        self.__database_server = database_server

    @property
    def is_async_env(self) -> bool:
        return self.__is_async_env

    @is_async_env.setter
    def is_async_env(self,is_async_env:bool):
        self.__is_async_env=is_async_env

    @property
    def database_url(self) -> str:
        if self.is_async_env:
            if self.database == "sqlite":
                return "sqlite+aiosqlite://"
            return f"{self.connector}+{self.database_async_connector}://{self.database_username}:{self.database_password}@{self.server}"
        else:
            if self.database == "sqlite":
                return "sqlite://"
            return f"{self.connector}://{self.database_username}:{self.database_password}@{self.server}"

    def create_sync_db(self):
        engine = create_engine(self.database_url, pool_pre_ping=True)
        conn = engine.connect()
        try:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database_name}"))
        finally:
            conn.close()

    async def create_async_db(self):
        engine = create_async_engine(self.database_url, pool_pre_ping=True)
        async with engine.begin() as conn:
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database_name}"))

    def create_database_if_not_exists(self):
        if self.database!="sqlite":
            if self.is_async_env:
                try:
                    loop=asyncio.get_running_loop()
                    loop.create_task(self.create_async_db())
                except RuntimeError:
                    asyncio.run(self.create_async_db())
            else:
                self.create_sync_db()

    @property
    def sqlalchemy_url(self):
        db = f"{self.database_url}/{self.database_name}"
        if self.database!='sqlite':
            return db
        else :
            return f"{db}.db"

    @property
    def engine(self):
        if self.is_async_env:
            engine = create_async_engine(self.sqlalchemy_url, pool_pre_ping=True)
        else:
            engine = create_engine(self.sqlalchemy_url, pool_pre_ping=True)
        return engine

    def create_session_manager(self):
        if self.is_async_env:
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine,expire_on_commit=True,class_=AsyncSession)
            session_manager=SessionManager(
                session_maker=sessionLocal,
                is_async_env=True
            )
        else:
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            session_manager = SessionManager(
                session_maker=sessionLocal, is_async_env=False
            )
        self.__session_manager=session_manager


    async def create_async_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    def create_tables(self):
        if self.is_async_env:
            try:
                loop=asyncio.get_running_loop()
                loop.create_task(self.create_async_tables())
            except RuntimeError:
                asyncio.run(self.create_async_tables())
        else:
            self.__target_metadata.create_all(bind=self.engine)
