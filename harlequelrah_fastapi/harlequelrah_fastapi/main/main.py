from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
# from myproject.settings.database import engine, authentication, sessionLocal
from myproject.settings.models_metadata import target_metadata
from harlequelrah_fastapi.middleware.error_middleware import ErrorHandlingMiddleware
from myproject.myappp.router import app_myapp

app = FastAPI()

target_metadata.create_all(bind=engine)


app.include_router(app_myapp)
app.add_middleware(
    ErrorHandlingMiddleware,
)

