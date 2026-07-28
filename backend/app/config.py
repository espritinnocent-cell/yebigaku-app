import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env ファイルを強制的に読み込む（確実な方法）
load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
