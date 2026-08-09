from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where this settings.py file is located, then navigate to server/.env
ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")
    DB_CONNECTION: str
    SECRET_KEY: str
    ALGORITHM: str
    EXP_TIME: int
    FINNHUB_API_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

settings = Settings()
