from pathlib import Path
from typing import List
from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn = Field(
        "postgresql://postgres:postgres@localhost:5432/ai_radar",
        env="DATABASE_URL",
    )
    llm_api_key: str = Field("", env="LLM_API_KEY")
    llm_model: str = Field("gpt-4o-mini", env="LLM_MODEL")
    cors_origins: str = Field("http://localhost:3000", env="CORS_ORIGINS")

    model_config = {
        "extra": "ignore",
        "env_file": str(Path(__file__).resolve().parents[2] / ".env"),
        "env_file_encoding": "utf-8",
    }

    @field_validator("cors_origins")
    def normalize_cors_origins(cls, value: str) -> str:
        return value.strip()

    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
