from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    class Config:
        env_file = "service/dev/.env"


settings = Settings()

engine = create_engine(settings.database_url)
session = sessionmaker(bind=engine)


# generator to be used as a FastAPI dependency
def get_session() -> Session:
    with session:
        yield session
