from fastapi import FastAPI
from .settings.database import engine, authentication
from .settings.models_metadata import target_metadata
from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware
# from myproject.myapp.router import app_myapp

app = FastAPI()

target_metadata.create_all(bind=engine)

@app.get("/")
async def hello():
    return {"message":"hello"}
# app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)

