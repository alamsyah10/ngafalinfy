import os
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # Application
    API_NAME: str = "NGAFALINFY API"
    ENV: str = "local"
    VERSION: str = "0.0.1"
    DEBUG: bool = True

    # CORS
    CORS_ALLOW_ORIGINS: str = ""

    def get_cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGINS.split(",")

    # Session
    SESSION_SECRET: str = ""
    SESSION_SAMESITE: Literal["lax", "strict", "none"] = "none"
    SESSION_HTTPS_ONLY: bool = False

    # Database (MySQL)
    SQL_LOGGING: bool = False
    MYSQL_HOST: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = ""

    def get_database_args(self) -> dict:
        args = {}
        # Specifying SSL certificate when connecting to Azure DB for MySQL
        # https://learn.microsoft.com/ja-jp/azure/mysql/single-server/how-to-configure-ssl
        if "mysql.database.azure.com" in self.MYSQL_HOST:
            project_root = os.getcwd()
            args["ssl_ca"] = f"{project_root}/certs/DigiCertGlobalRootG2.crt.pem"
        return args

    def get_database_url(self, db_prefix: str = "", user: str = "") -> str:
        db_name = (
            f"{db_prefix}_{self.MYSQL_DATABASE}" if db_prefix else self.MYSQL_DATABASE
        )
        db_user = user if user else self.MYSQL_USER
        return f"mysql+pymysql://{db_user}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{db_name}?charset=utf8mb4"

    # JWT
    JWT_SECRET: str = ""
    JWT_EXPIRES_MIN: int = 60
    ALG: str = ""
    COOKIE_NAME: str = ""

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
