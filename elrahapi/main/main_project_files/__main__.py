import uvicorn
from app.settings.config.env_config import settings

if __name__ == "__main__":
    uvicorn.run(
        f"app.main:app",
        host=settings.host,
        port=8000,
        reload=settings.debug,
    )
