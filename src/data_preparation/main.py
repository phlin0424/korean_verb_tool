import json

from korean_verb_tool.utils.audio import AudioCreator
from korean_verb_tool.config import settings

if __name__ == "__main__":
    tts_input_csv = settings.mp3_path / "output_word_list.csv"
    with tts_input_csv.open() as f:
        input_text_list = f.read()
    input_text_list = input_text_list.split("\n")

    verb_origin_csv = settings.mp3_path / "word_list.csv"
    with verb_origin_csv.open() as f:
        word_list = f.read()
    word_list = word_list.split("\n")

    audio_creator = AudioCreator()

    data_list = []
    for input_text, word in zip(input_text_list, word_list, strict=False):
        # print(input_text, word)
        response = audio_creator.create_audio(input_text)
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
    with file_path.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)  # 'indent=4' makes the JSON human-readable
