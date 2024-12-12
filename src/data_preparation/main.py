from korean_verb_tool.config import settings
from korean_verb_tool.audio import AudioCreator


if __name__ == "__main__":
    with open(settings.mp3_path / "output_word_list.csv", "r") as f:
        word_list = f.read()

    word_list = word_list.split("\n")
