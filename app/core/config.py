from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ATLAS"
    app_env: str = "development"
    debug: bool = True

    
    model_name: str = "openai/gpt-oss-120b"
    GROQ_API_KEY: str = "YOUR_API_KEY"
    model_temperature: float = 0.7
    model_max_tokens: int = 1000
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()