import uvicorn
import os
from dotenv import load_dotenv

load_dotenv(".env")
project_name = os.getenv("PROJECT_NAME")
env=os.getenv("ENV")
if __name__ == "__main__":
    uvicorn.run(f"{project_name}.main:app", host="127.0.0.1", port=8000, reload=(env=="dev"))
