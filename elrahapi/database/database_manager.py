from elrahapi.database.session_manager import SessionManager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


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
    ):
        self.__database = database
        self.__database_username = database_username
        self.__database_password = database_password
        self.__database_connector = database_connector
        self.__database_async_connector = database_async_connector
        self.database_name = database_name
        self.__database_server = database_server

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
        if self.database == "sqlite" and database_name is None:
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
        return self.__database_async_connector is not None

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

    def create_database_if_not_exists(self):
        if self.is_async_env:
            engine = create_async_engine(self.database_url, pool_pre_ping=True)
        else:
            engine = create_engine(self.database_url, pool_pre_ping=True)
        conn = engine.connect()
        try:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.database_name}"))
        finally:
            conn.close()

    @property
    def sqlalchemy_url(self):
        return f"{self.database_url}/{self.database_name}"

    def create_session_maker(self):
        if self.is_async_env:
            engine = create_async_engine(self.sqlalchemy_url, pool_pre_ping=True)
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=True,class_=AsyncSession)
        else:
            engine = create_engine(self.sqlalchemy_url, pool_pre_ping=True)
            sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session_manager = SessionManager(
                session_maker=sessionLocal, is_async_env=False
            )
        return session_manager
