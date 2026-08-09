from pathlib import Path
from pydantic import BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn = Field(..., env="DATABASE_URL")
    llm_api_key: str = Field("", env="LLM_API_KEY")
    llm_model: str = Field("gpt-4o-mini", env="LLM_MODEL")

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
