import json
from pathlib import Path

import streamlit as st

from korean_verb_tool.config import settings

# Open and read the JSON file
with (settings.mp3_path / "test.json").open(encoding="utf-8") as json_file:
    data = json.load(json_file)


def mp3_player(text: str, mp3_filename: Path) -> None:
    """Display the mp3 player widget.

    Args:
        text (str): _description_
        mp3_filename (Path): _description_
    """
    # MP3 file to play
    audio_file_path = settings.mp3_path / mp3_filename

    # Load and play the audio file
    with audio_file_path.open("rb") as audio_file:
        audio_bytes = audio_file.read()

    st.text(text)
    st.audio(audio_bytes, format="audio/mp3")


# Set the title
st.title("Simple MP3 Player")

# Streamlit's audio player
for item in data["data"]:
    word = item["word"]
    mp3_filename = item["mp3"]
    mp3_player(word, mp3_filename)
