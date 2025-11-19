import asyncio

from elrahapi.database.session_manager import SessionManager
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta


class DatabaseManager:

    def __init__(
        self,
        database: str,
        database_name: str,
        database_server: str = "",
        database_async_connector: str = "",
        database_username: str = "",
        database_password: str = "",
        is_async_env: bool = False,
        database_connector: str = "",
        env: str = "dev",
        database_creation_script: str | None = None,
    ):
        self.__env = env
        self.__database = database
        self.__database_username = database_username
        self.__database_password = database_password
        self.__database_connector = database_connector
        self.__database_async_connector = database_async_connector
        self.__database_name = self.setup_database_name(database_name)
        self.__database_server = database_server
        self.__session_manager: SessionManager = None
        self.__is_async_env = (
            True if is_async_env is True and self.__database_async_connector else False
        )
        self.__create_database_if_not_exists_text = None
        if database_creation_script:
            self.__create_database_if_not_exists_text = text(database_creation_script)

    @property
    def session_manager(self):
        return self.__session_manager

    @session_manager.setter
    def session_manager(self, session_manager: SessionManager):
        self.__session_manager = session_manager

    @property
    def env(self):
        return self.__env

    @env.setter
    def env(self, env: str):
        self.__env = env

    def setup_database_name(self, database_name) -> str:
        if self.__env == "test":
            return "test_database"
        else:
            if self.__database == "sqlite" and not database_name:
                return "database"
            else:
                return database_name

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
    def is_async_env(self, is_async_env: bool):
        self.__is_async_env = is_async_env

    @property
    def database_url(self) -> str:
        if self.is_async_env:
            if self.__database == "sqlite":
                return "sqlite+aiosqlite://"
            return f"{self.database_connector}+{self.database_async_connector}://{self.database_username}:{self.database_password}@{self.database_server}"
        else:
            if self.__database == "sqlite":
                return "sqlite://"
            else:
                return f"{self.database_connector}://{self.database_username}:{self.database_password}@{self.database_server}"

    def create_sync_db(self):
        engine = create_engine(self.database_url, pool_pre_ping=True)
        conn = engine.connect()
        try:
            conn.execute(self.__create_database_if_not_exists_text)
        finally:
            conn.close()

    async def create_async_db(self):
        engine = create_async_engine(self.database_url, pool_pre_ping=True)
        async with engine.begin() as conn:
            await conn.execute(self.__create_database_if_not_exists_text)

    def create_database_if_not_exists(self):
        try:
            if (
                self.__database != "sqlite"
                and self.__create_database_if_not_exists_text is not None
            ):
                if self.is_async_env:
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(self.create_async_db())
                    except RuntimeError:
                        asyncio.run(self.create_async_db())
                else:
                    self.create_sync_db()
        except Exception as exc:
            print(f"Error creating database: {exc}")

    @property
    def sqlalchemy_url(self):
        db = f"{self.database_url}/{self.database_name}"
        if self.__database != "sqlite":
            return db
        else:
            return f"{db}.db"

    @property
    def engine(self):
        if self.__is_async_env:
            engine = create_async_engine(self.sqlalchemy_url, pool_pre_ping=True)
        else:
            engine = create_engine(self.sqlalchemy_url, pool_pre_ping=True)
        return engine

    def create_session_manager(self):
        if self.is_async_env:
            sessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                expire_on_commit=True,
                class_=AsyncSession,
            )
            session_manager = SessionManager(
                session_maker=sessionLocal, is_async_env=True
            )
        else:
            sessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            session_manager = SessionManager(
                session_maker=sessionLocal, is_async_env=False
            )
        self.__session_manager = session_manager

    async def create_async_tables(self, target_metadata: MetaData):
        async with self.engine.begin() as conn:
            await conn.run_sync(target_metadata.create_all)

    def drop_tables(self, target_metadata: MetaData):
        target_metadata.drop_all(bind=self.engine)

    def create_target_metadata(self, bases: list[DeclarativeMeta]):
        target_metadata = MetaData()
        for base in bases:
            for table in sorted(
                base.metadata.tables.values(), key=lambda t: len(t.foreign_keys)
            ):
                table.tometadata(target_metadata)
        return target_metadata

    def create_tables(self, target_metadata: MetaData):
        if self.is_async_env:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.create_async_tables(target_metadata))
            except RuntimeError:
                asyncio.run(self.create_async_tables(target_metadata))
            except Exception:
                pass
        else:
            try:
                target_metadata.create_all(bind=self.engine)
            except Exception as e:
                print(f"{str(e)}")
                pass
