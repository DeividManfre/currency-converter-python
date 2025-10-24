from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    currency_api_key: str
    currency_api_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()