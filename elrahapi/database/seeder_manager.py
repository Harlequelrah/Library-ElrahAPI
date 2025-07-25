from elrahapi.database.session_manager import SessionManager
from elrahapi.utility.types import ElrahSession
from elrahapi.utility.utils import get_pks
from pydantic import BaseModel
from elrahapi.crud.crud_forgery import CrudForgery
class Seed:

    def __init__(self, crud_forgery: CrudForgery, data: list[BaseModel]):
        self.crud_forgery = crud_forgery
        self.data = data
        self.pk_list = []

    async def up(self,session:ElrahSession):
        created_data = await self.crud_forgery.bulk_create(create_obj_list=self.data,session=session)
        self.pk_list = get_pks(l=created_data,pk_name=self.crud_forgery.primary_key_name)

    async def down(self, session: ElrahSession):
        await self.crud_forgery.bulk_delete(pk_list=self.pk_list)

class SeedManager:
    def __init__(self,seeds_dict:dict[str,Seed],session_manager:SessionManager):
        self.seeds_dict= seeds_dict
        self.session_manager = session_manager

    async def up(self,full_seeds:bool=True,seeds_name:list[str]|None=None):
        await self.run(
            seeds_name=seeds_name,
            full_seeds=full_seeds,
            up=True
        )

    async def down(self, full_seeds: bool = True, seeds_name: list[str] | None = None):
        await self.run(
            full_seeds=full_seeds,
            seeds_name=seeds_name,
            up=False
        )
    async def run(self, up:bool,full_seeds: bool = True, seeds_name: list[str] | None = None):
        try:
            session = await self.session_manager.get_session()
            seeds = (
                self.seeds_dict.values()
                if full_seeds
                else [
                    seed[seed_name]
                    for seed_name in self.seeds_dict
                    if seed_name in seeds_name
                ]
            )
            for seed in seeds:
                await seed.up(session) if up else seed.down(session)
        except:
            await self.session_manager.rollback_session(session)
        finally:
            await self.session_manager.close_session(session)


