from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Feature Flag Management System"
    debug: bool = True

    db_user: str = "ff_user"
    db_password: str = "ff_password"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "feature_flags"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
