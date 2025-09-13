from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Courier - LEON ROLDAN"
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./courier.db"
    SECRET_KEY: str = "supersecretcourier3147246"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()
