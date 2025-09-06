import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    API_NAME: str = "NGAFALINFY API"
    ENV: str = "local"
    VERSION: str = "0.0.1"
    CORS_ALLOW_ORIGINS: str = ""
    DEBUG: bool = True
    SQL_LOGGING: bool = False
    MYSQL_HOST: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = ""

    def get_database_args(self) -> dict:
        args = {}
        # Azure DB for MySQL に接続するときのSSL証明書を指定する。
        # https://learn.microsoft.com/ja-jp/azure/mysql/single-server/how-to-configure-ssl
        if "mysql.database.azure.com" in self.MYSQL_HOST:
            project_root = os.getcwd()
            args["ssl_ca"] = f"{project_root}/certs/DigiCertGlobalRootG2.crt.pem"
        return args

    def get_database_url(self, db_prefix="", user="") -> str:
        db_name = (
            f"{db_prefix}_{self.MYSQL_DATABASE}" if db_prefix else self.MYSQL_DATABASE
        )
        db_user = user if user else self.MYSQL_USER
        return f"mysql+pymysql://{db_user}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/{db_name}?charset=utf8mb4"

    def get_cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGINS.split(",")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
