import os
from dotenv import load_dotenv
from pathlib import Path

env_path= Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    POSTGRES_USER: str=os.getenv("POSTGRES_USER","postgres")
    POSTGRES_PASSWORD: str =os.getenv("POSTGRES_PASSWORD","postgres")
    POSTGRES_SERVER: str=os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT: str=os.getenv("POSTGRES_PORT",5432)
    POSTGRES_DB: str=os.getenv("POSTGRES_DB","test")
    DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}")
    SECRET_KEY: str=os.getenv("SECRET_KEY","09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = os.getenv("ALGORITHM","HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: float = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30)

settings = Settings()
