class PromptManager:
    def __init__(self) -> None:
        # Basic prompt
        self.prompts = """
        与えられた韓国語の動詞単語を否定型で出力してください。
        出力の形式は~지않습니다,안 ~습니다にしてください。
        単語と単語の合間は、スペースは抜いてコンマだけ入れてください。
        例えば、下記の動詞が入力された：
        {example_verb}
        下記の出力を返してください：
        {example_variance}
        """

        # One shot example for AI
        self.one_shot = {
            "negative_verb_gen": ["하다", "하지않습니다,안 합니다"],
        }

    def __get_kwarg_dict(self, name: str) -> dict[str, str]:
        # A helper function to retrieve the dict for generating prompt.
        example_list = self.one_shot.get(name)
        if example_list is None:
            raise KeyError
        return {"example_verb": example_list[0], "example_variance": example_list[1]}

    @property
    def negative_verb_prompt(self) -> str:
        """韓国語動詞の否定形を取得する用プロント.

        Returns:
            str: プロント
        """
        return self.prompts.format(**self.__get_kwarg_dict("negative_verb_gen"))
