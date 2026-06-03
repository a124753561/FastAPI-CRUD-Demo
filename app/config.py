from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI CRUD Demo"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/demo"
    DEBUG: bool = False

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
