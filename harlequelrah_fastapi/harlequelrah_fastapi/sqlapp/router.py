from sqlalchemy.orm import Session
from myproject.settings.database import authentication
from myproject.myapp.crud import myapp_crud
import myproject.myapp.model as model
from fastapi import Depends, APIRouter
from typing import List
from harlequelrah_fastapi.router.router_provider import provide_router,ProvideRouter

app_todolist = ProvideRouter(
    prefix="/todoitem",
    tags=["todo"],
    PydanticModel=model.PydanticModel,
    crud=myapp_crud,
    authentication=authentication,
)

provide_router.initialize_router(
    {
        "create": True,
        "update": True,
        "count": True,
        "read-one": True,
        "read-all": True,
        "read-all-by-filter": True,
        "delete": True,
    }
)
app_myapp = provide_router.router
