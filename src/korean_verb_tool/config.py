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

    db_host: str
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def postgres_local_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@localhost/{self.postgres_db}"

    model_config = SettingsConfigDict(
        env_file=DIR_PATH / ".env",
        env_file_encoding="utf-8",
    )


settings = Config()
