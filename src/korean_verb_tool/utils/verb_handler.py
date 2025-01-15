from pydantic_ai import Agent
from pydantic_ai.models import Model

from korean_verb_tool.utils.prompt_manager import PromptManager


class KoreanVerbHandler:
    def __init__(self, model: Model) -> None:
        """Initialize a verb handler.

        Args:
            model (Model): Pydantic ai model
        """
        self.model = model
        self.prompt = PromptManager()

    async def to_negative(self, verb: str) -> str:
        """Function to generate negative form of the input korean verb.

        Args:
            verb (str): Korean verb.

        Returns:
            str: _description_
        """
        # Prompt for generating negative form of the specific verb
        prompt = self.prompt.negative_verb_prompt

        # Initialize an agent based on the prompt
        agent = Agent(self.model, system_prompt=prompt)

        # Make a request
        result = await agent.run(verb)

        # Remove \n symbol if exists
        return result.data.split("\n")[0]

    async def to_to_honorific() -> str:
        pass
