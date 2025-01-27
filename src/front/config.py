from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DIR_PATH = Path(__file__).resolve().parent
MP3_PATH = Path(__file__).resolve().parent.parent / "data"


class Config(BaseSettings):
    api_server_url: str = Field(description="The api server url.")

    mp3_path: Path = Field(
        default=MP3_PATH,
        description="Data lake for storing the audio mp3 files.",
    )

    model_config = SettingsConfigDict(
        env_file=DIR_PATH / ".env",
        env_file_encoding="utf-8",
    )


settings = Config()
