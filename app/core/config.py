from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    currency_api_key: str
    currency_api_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()