from fastapi import FastAPI
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
from .settings.models_metadata import target_metadata

# from .myapp.router import app_myapp
from .settings.database import database

database.create_tables(target_metadata=target_metadata)
app = FastAPI(
    root_path="/api"
)


@app.get("/")
async def hello():
    return {"message": "hello"}


# app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)
