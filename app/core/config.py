from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ATLAS"
    app_env: str = "development"
    debug: bool = True

    '''postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "atlas"
    postgres_user: str = "atlas"
    postgres_password: str = "change_me"

    mongodb_uri: str = "mongodb://mongodb:27017"
    mongodb_db: str = "atlas"
    jwt_secret_key: str = "your-super-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    enable_chat_graph: bool = False

    faiss_index_path: str = "./faiss_index"
    embedding_model_name: str = "findme"'''
    GROQ_API_KEY: str = "YOUR_API_KEY"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()