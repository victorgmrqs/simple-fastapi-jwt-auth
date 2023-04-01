from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Curso FastAPI - Segurança'
    PROJECT_DESCRIPTION: str = 'Projeto básico para segunraça com FastAPI'
    PROJECT_VERSION: str = '0.0.1'

    DB_URL: str = 'postgresql+asyncpg://postgres:mysecretpassword@localhost:5431/faculdade'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'n6zkK17BwjftaaiI2SgJ0iGpAq_mCK8MQuhfff0nv_Y'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        case_sesitive = True


settings: Settings = Settings()


"""
    import secrets
    
    token: str = secrets.url_token(32)
    'n6zkK17BwjftaaiI2SgJ0iGpAq_mCK8MQuhfff0nv_Y'
    
"""
