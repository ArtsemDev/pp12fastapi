from pydantic import SecretStr, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_STR: SecretStr
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    TOKEN_TYPE: str
    ALGORITHM: str
    ACCESS_EXP_TOKEN: int
    REFRESH_EXP_TOKEN: int
