import uuid
from pathlib import Path

from navertts import NaverTTS

from korean_verb_tool.config import settings


class AudioCreator:
    def __init__(self, lang: str = settings.using_lang) -> None:
        self.lang = lang

    def create_audio(
        self,
        input_text: str,
        path: Path | str = settings.mp3_path,
    ) -> Path:
        """Create an audio file (.mp3) for the input korean word. Using on Naver TTS API.

        Args:
            input_text (str): _description_
            path (Path | str, optional): _description_. Defaults to settings.mp3_path.

        Returns:
            Path | str: The path of the output audio file.
                For example: User/path/to/directory/naver_e9633695-8fce-4ea3-901a-489863a9214e.mp3
        """
        # Validate the path
        if not isinstance(path, Path):
            path = Path(path)

        # Create the dictionary if not existing
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        # Create the audio
        tts = NaverTTS(input_text)

        # Create a unique ID, use it to create the mp3 filename ID
        unique_id = uuid.uuid5(settings.namespace_uuid, input_text)
        filename = f"{unique_id}.mp3"
        audio_filename = path / filename

        # Save the audio file
        tts.save(audio_filename)

        return audio_filename
