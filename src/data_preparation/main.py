from korean_verb_tool.audio import AudioCreator
from korean_verb_tool.config import settings
import json

if __name__ == "__main__":
    with open(settings.mp3_path / "output_word_list.csv", "r") as f:
        inut_text_list = f.read()
    inut_text_list = inut_text_list.split("\n")

    with open(settings.mp3_path / "word_list.csv", "r") as f:
        word_list = f.read()
    word_list = word_list.split("\n")

    ausdio_creator = AudioCreator()

    data_list = []
    for input_text, word in zip(inut_text_list, word_list):
        # print(input_text, word)
        response = ausdio_creator.create_audio(input_text)
        mp3_filename = str(response.name)
        data_list.append(
            {
                "word": word,
                "variant": input_text,
                "mp3": mp3_filename,
            }
        )

    data = {"data": data_list}

    file_path = settings.mp3_path / "test.json"
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)  # 'indent=4' makes the JSON human-readable
