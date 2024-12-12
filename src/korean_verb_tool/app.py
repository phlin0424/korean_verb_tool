import streamlit as st
from korean_verb_tool.config import settings

# Set the title
st.title("Simple MP3 Player")

# MP3 file to play
audio_file_path = settings.mp3_path / "naver_7e9d0030-dc34-4924-9080-60f14c2d23e5.mp3"  # Path to your MP3 file

# Load and play the audio file
with open(audio_file_path, "rb") as audio_file:
    audio_bytes = audio_file.read()

# Streamlit's audio player
st.text("듣다")
st.audio(audio_bytes, format="audio/mp3")
