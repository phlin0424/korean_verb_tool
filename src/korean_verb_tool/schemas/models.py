from enum import Enum

from pydantic import BaseModel, Field


class InputLang(str, Enum):
    ko = "ko"


class TranslatedLang(str, Enum):
    en = "en"
    ja = "ja"


class QueryResponse(BaseModel):
    """A data model for the response of a query to a repository."""

    origin: str = Field(default=None, description="Original form")
    audio: str = Field(default=None, description="The query result: Audio file name")
    variance: str = Field(default=None, description="The query result: the variance of the verb.")


class PostQuery(BaseModel):
    """A data model of a query to execute posting action to a variance table repository."""

    origin: str = Field(default=None, description="Original form")
    variance: str | None = Field(default=None, description="Negative form (or other variance) of the input verb")
    audio: str | None = Field(default=None, description="Negative form (or other variance) of the input verb")
