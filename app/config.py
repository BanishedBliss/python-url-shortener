from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SERVICE_TIMEOUT: float = 5.0
    HOST: str = "127.0.0.1"
    PORT: int = 8080

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()