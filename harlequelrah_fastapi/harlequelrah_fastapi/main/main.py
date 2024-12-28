from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
# from myproject.settings.database import engine, authentication, sessionLocal
from myproject.settings.models_metadata import target_metadata
from harlequelrah_fastapi.middleware.error_middleware import ErrorHandlingMiddleware
# from myproject.todolistapp.router import app_todolist

app = FastAPI()

target_metadata.create_all(bind=engine)


app.include_router(app_todolist)
app.add_middleware(
    ErrorHandlingMiddleware,
)

