from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "Nexus Workforce"
    API_VERSION: str = "3.1.0"
    DATABASE_URL: str = "sqlite:///./nexus_workforce.db"
    CONTACT_EMAIL: str = "ops@nexusworkforce.dev"
    ENABLE_DOCS: bool = True
    CORS_ORIGINS: list[str] = ["*"]

    model_config = {"env_prefix": "NEXUS_"}


settings = AppSettings()
