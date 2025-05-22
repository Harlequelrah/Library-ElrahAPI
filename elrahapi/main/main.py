from fastapi import FastAPI
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware

# from .myapp.router import app_myapp
from .settings.models_metadata import database

database.create_tables()

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "hello"}


# app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)
