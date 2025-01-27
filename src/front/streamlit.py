import json
from pathlib import Path

import streamlit as st

from front.client import KoreanVerbNegativeClient
from front.config import settings


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


def verbs_player_page() -> None:
    """A page for the verbs listed in a json file players."""
    # Open and read the JSON file
    with (settings.mp3_path / "test.json").open(encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Set the title
    st.title("韓国語否定語練習")

    # Streamlit's audio player
    for item in data["data"]:
        word = item["word"]
        mp3_filename = item["mp3"]
        mp3_player(word, mp3_filename)


def practice_page() -> None:
    """A page for requesting random api endpoint."""
    if "action" not in st.session_state:
        st.session_state.action = False

    client = KoreanVerbNegativeClient()
    response = client.get_random_verb()

    # Set the title
    st.title("韓国語否定語練習")

    # Streamlit's audio player
    if st.button("TRY IT"):
        st.session_state.action = True
        word = response["origin"]
        mp3_filename = response["audio"]

    if st.session_state.action:
        mp3_player(word, mp3_filename)


# Page dictionary
pages = {"Verb List": verbs_player_page, "Practice": practice_page}

# Sidebar with a drop-down list for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Go to", list(pages.keys()))

# Display the selected page
page = pages[selection]
page()
