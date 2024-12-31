from pydantic_ai import Agent
from korean_verb_tool.config import settings
from korean_verb_tool.utils.prompt_manager import PromptManager
from pydantic_ai.models.gemini import GeminiModel

# TODO: Enable other types of models also: https://ai.pydantic.dev/models/
model = GeminiModel("gemini-1.5-flash", api_key=settings.gemini_api_key)


async def generate_negative_variance(verb: str) -> str:
    # Prompt for generating negative form of the specific verb
    prompt = PromptManager().negative_verb_prompt

    # Initialize an agent based on the prompt
    agent = Agent(model, system_prompt=prompt)

    # Make a request
    result = await agent.run(verb)

    return result.data
