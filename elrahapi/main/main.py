from elrahapi.middleware.error_middleware import ErrorHandlingMiddleware

# from myapp.router import myapp_router
from settings.database import database

from fastapi import FastAPI

app = FastAPI(root_path="/api")


@app.get("/")
async def hello():
    return {"message": "hello"}


# app.include_router(myapp_router)
app.add_middleware(
    ErrorHandlingMiddleware,
)
