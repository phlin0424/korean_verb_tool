import asyncio

from pydantic import BaseModel, Field, model_validator
from pydantic_ai.models.gemini import GeminiModel

from korean_verb_tool.config import settings
from korean_verb_tool.utils.verb_handler import KoreanVerbHandler

# TODO: Enable other types of models also: https://ai.pydantic.dev/models/
model = GeminiModel(settings.AI_model, api_key=settings.gemini_api_key)

# Initialize the korean verb handler
korean_verb_handler = KoreanVerbHandler(model)


class Vocabulary(BaseModel):
    """A data model when inserting a new row into the db."""

    origin: str = Field(default=None, description="Original form")
    negative: str = Field(default=None, description="Negative form of the input verb")
    honorific: str = Field(default=None, description="Honorific form of the input verb")

    @model_validator(mode="after")
    def transform_to_negative(self) -> "Vocabulary":
        """Convert the verb into a negative form automatically.

        Returns:
            _type_: _description_
        """
        if self.negative is None:
            origin = self.origin
            self.negative = asyncio.run(korean_verb_handler.to_negative(origin))
        return self


if __name__ == "__main__":
    voc = Vocabulary(origin="마시다")
    print(voc)
