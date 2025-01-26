from pydantic import BaseModel, Field


class NegativeFormResponse(BaseModel):
    origin: str = Field(default=..., description="韓国語の原型動詞（〜다）")
    negative: str = Field(default=None, description="動詞の否定形")
    audio: str = Field(default=None, description="動詞の否定形の音声ファイル名")


class VerbQuery(BaseModel):
    origin: str = Field(default=..., description="韓国語の原型動詞（〜다）")


class VerbPost(BaseModel):
    origin: str = Field(default=..., description="韓国語の原型動詞（〜다）")
    negative: str | None = Field(default=None, description="動詞の否定形")
    audio: str | None = Field(default=None, description="動詞の否定形の音声ファイル名")
