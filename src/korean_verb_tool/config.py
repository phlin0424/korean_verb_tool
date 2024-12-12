import uuid
from pathlib import Path
from uuid import UUID

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

from korean_verb_tool.models import InputLang, TranslatedLang

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

    model_config = ConfigDict(protected_namespaces=("settings_",))


settings = Config()
