
from fastapi import FastAPI
import uvicorn
from settings.database import engine, authentication
# from settings import logger_model # activer les logs
# from myapp import models
from sqlalchemy import MetaData
# from userapp import user_model # utiliser l'application utilisateur
# from userapp.app_user import app_user # utiliser l'application utilisateur
from harlequelrah_fastapi.middleware.error_middleware import ErrorHandlingMiddleware # activer le middleware de gestion d'erreur
# from harlequelrah_fastapi.middleware.log_middleware import LoggerMiddleware # activer le middleware de gestions logs
# from myapp.route import app_myapp importer le router de votre application

app = FastAPI()
target_metadata = MetaData()
# target_metadata = models.Base.metadata
# target_metadata = logger_model.Base.metadata metadata pour la table loggers
# target_metadata = user_model.Base.metadata  #metadata pour la table users
target_metadata.create_all(bind=engine)





# app.include_router(app_user) # routes pour appuser
# app.include_router(app_myapp) #routes pour myapp
# app.add_middleware(
#     LoggerMiddleware,
#     LoggerMiddlewareModel=logger_model.Logger,
#     db_session=authentication.get_session,
# ) #middleware pour les logs
app.add_middleware(ErrorHandlingMiddleware)


if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", port=8000, reload=True)
