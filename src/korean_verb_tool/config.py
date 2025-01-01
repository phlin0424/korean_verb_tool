import uuid
from pathlib import Path
from uuid import UUID

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from korean_verb_tool.schemas.models import InputLang, TranslatedLang

DIR_PATH = Path(__file__).resolve().parent.parent
MP3_PATH = DIR_PATH / "data"


class Config(BaseSettings):
    dir_path: Path = Field(
        default=DIR_PATH,
        description="The directory path for the application. (src/...)",
    )

    mp3_path: Path = Field(
        default=DIR_PATH / "data",
        description="The directory path for the TTS generate audios.",
    )

    using_lang: InputLang = Field(
        default=InputLang.ko,
        description="The default input language.",
    )

    translate_lang: TranslatedLang = Field(
        default=TranslatedLang.ja,
        description="The translating language.",
    )

    namespace_uuid: UUID = Field(
        default=uuid.NAMESPACE_DNS,
        description="Namespace UUID for deterministic filename generation.",
    )

    AI_model: str = Field(default="gemini-1.5-flash", description="LLM name.")
    db_host: str = Field(description="Host for PostgreSQL DB.")
    postgres_user: str = Field(description="PostgreSQL DB username.")
    postgres_password: str = Field(description="PostgreSQL DB password. ")
    postgres_db: str = Field(description="PostgreSQL DB name.")
    aws_access_key_id: str = Field(description="Access key to connect to AWS")
    aws_secret_access_key: str = Field(description="Secret key to connect to AWS")
    openai_api_key: str = Field(description="Open AI API key.")
    gemini_api_key: str = Field(description="Gemini API key.")

    @property
    def postgres_local_url(self) -> str:
        """Postgres db local url.

        Returns:
            str: _description_
        """
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@localhost/{self.postgres_db}"

    model_config = SettingsConfigDict(
        env_file=DIR_PATH / ".env",
        env_file_encoding="utf-8",
    )


settings = Config()
