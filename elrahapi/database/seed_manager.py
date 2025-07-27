from elrahapi.database.session_manager import SessionManager
from elrahapi.utility.types import ElrahSession
from elrahapi.utility.utils import  get_pks
from pydantic import BaseModel
from elrahapi.crud.crud_forgery import CrudForgery
import asyncio
import re
from elrahapi.crud.bulk_models import BulkDeleteModel
from logging import Logger

class Seed:

    def __init__(
        self, crud_forgery: CrudForgery, data: list[BaseModel], logger: Logger,seeders_logs:str
    ):
        self.crud_forgery = crud_forgery
        self.data = data
        self.logger = logger
        self.seeders_logs = seeders_logs




    async def up(self, session: ElrahSession):
        created_data = await self.crud_forgery.bulk_create(
            create_obj_list=self.data, session=session
        )
        pk_list = get_pks(l=created_data, pk_name=self.crud_forgery.primary_key_name)
        self.logger.info(
            f"Seeded {self.crud_forgery.entity_name} - with {len(pk_list)} records successfully . PKS:{pk_list}"
        )

    def get_pks_list(self):
        entity_name = self.crud_forgery.entity_name.lower()
        with open(self.seeders_logs, "r") as file:
            lines = file.readlines()
        # On parcourt les lignes à l'envers
        for line in reversed(lines):
            if f"seeded {entity_name} - with" in line.lower():
                match = re.search(r"PKS:\[(.*?)\]", line)
                if match:
                    pks_str = match.group(1)
                    # On split puis convertit en int
                    return [int(pk.strip()) for pk in pks_str.split(",") if pk.strip()]
        return []

    async def down(self, session: ElrahSession):
        delete_list = self.get_pks_list() or []
        pk_list = BulkDeleteModel(delete_list=delete_list)
        await self.crud_forgery.bulk_delete(session=session, pk_list=pk_list)
        self.logger.info(
            f"Rolled back {self.crud_forgery.entity_name} with {len(pk_list.delete_list)} records successfully."
        )

    async def start(self, action: str, session: ElrahSession):
        if action == "up":
            print("Executing seed up")
            await self.up(session)
        elif action == "down":
            print("Rollback")
            await self.down(session)
        else:
            print("Unknow action :", action)

    def run_seed(self, argv: list[str], session: ElrahSession):
        if len(argv) > 1:
            action = argv[1]
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.start(action, session))
            except RuntimeError:
                asyncio.run(self.start(action, session))
        else:
            print("No action provided, defaulting to 'up'")


class SeedManager:
    def __init__(self, seeds_dict: dict[str, Seed], session_manager: SessionManager):
        self.seeds_dict = seeds_dict
        self.session_manager = session_manager

    async def up(self, seeds_name: list[str] | None = None):
        await self.run(seeds_name=seeds_name, action=True)

    async def down(self, seeds_name: list[str] | None = None):
        await self.run(seeds_name=seeds_name, action=False)

    def run_seed_manager(self, argv: list[str],seeds_name: list[str] | None = None):
        action_name = argv[1] if len(argv) > 1 else "up"
        action = action_name.lower() == "up"
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.run(action=action, seeds_name=seeds_name))
        except RuntimeError:
            asyncio.run(
                self.run(action=action, seeds_name=seeds_name)
            )

    async def run(
        self,action:bool, seeds_name: list[str] | None = None
    ):
        try:
            session = await self.session_manager.get_session()
            seeds = (
                list(self.seeds_dict.values())
                if not seeds_name
                else [
                    self.seeds_dict.get(seed_name)
                    for seed_name in self.seeds_dict
                    if seed_name in seeds_name
                ]
            )
            if not action :
                seeds.reverse()
            for seed in seeds:
                if action :
                    await seed.up(session)
                else:
                    await seed.down(session)
        except:
            await self.session_manager.rollback_session(session)
        finally:
            await self.session_manager.close_session(session)
