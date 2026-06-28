from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AlgoGym"
    environment: str = "development"
    database_url: str = "sqlite:///./data/algogym.db"
    chroma_path: str = "./data/chroma"
    upload_dir: str = "./data/uploads"
    openai_base_url: str = "http://localhost:11434/v1"
    openai_api_key: str = "ollama"
    llm_model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ALGOGYM_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
