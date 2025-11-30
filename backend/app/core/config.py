import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ResearchMate AI"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

settings = Settings()
