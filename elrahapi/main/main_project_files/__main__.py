import uvicorn
from app.settings.config.env_config import settings

if __name__ == "__main__":
    uvicorn.run(
        f"{settings.project_name}.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.debug,
    )
