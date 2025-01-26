from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic_ai.models.gemini import GeminiModel
from sqlalchemy.ext.asyncio import AsyncSession

from korean_verb_tool.config import settings
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceNegativeTable
from korean_verb_tool.db.cruds import NegativeVerbRepository
from korean_verb_tool.db.session import get_db
from korean_verb_tool.schemas.apischemas import NegativeFormResponse, VerbPost, VerbQuery
from korean_verb_tool.schemas.models import PostQuery
from korean_verb_tool.utils.audio import AudioCreator
from korean_verb_tool.utils.verb_handler import KoreanVerbHandler

routers = APIRouter()


@routers.get("/negative_forms")
async def get_negative_forms(
    verb_query: Annotated[VerbQuery, Depends()],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> NegativeFormResponse:
    """Get the negative forms of the input original form of the korean verb."""
    nr = NegativeVerbRepository(
        db=session,
        main_table=KoreanVerbTable,
        variance_table=KoreanVerbVarianceNegativeTable,
    )

    try:
        result = await nr.get(verb_query.origin)
    except ValueError as e:
        error_msg = f"Korean verb '{verb_query.origin}' not found."
        raise HTTPException(status_code=404, detail=error_msg) from e

    # Construct the responses
    return NegativeFormResponse(
        origin=result.origin,
        negative=result.variance,
        audio=result.audio,
    )


@routers.get("/negative_forms_random")
async def get_negative_forms_random(session: Annotated[AsyncSession, Depends(get_db)]) -> NegativeFormResponse:
    """Get the negative forms randomly from the existing db.

    Args:
        session (Annotated[AsyncSession, Depends): _description_

    Returns:
        NegativeFormResponse: _description_
    """
    nr = NegativeVerbRepository(
        db=session,
        main_table=KoreanVerbTable,
        variance_table=KoreanVerbVarianceNegativeTable,
    )

    try:
        result = await nr.get_random_row()
    except ValueError as e:
        error_msg = f"Korean verb '{result.origin}' not found."
        raise HTTPException(status_code=404, detail=error_msg) from e

    # Construct the responses
    return NegativeFormResponse(
        origin=result.origin,
        negative=result.variance,
        audio=result.audio,
    )


@routers.post("/negative_forms")
async def post_negative_forms(
    verb: Annotated[VerbPost, Depends()],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> NegativeFormResponse:
    """Post a new verb as well as its negative variance.

    Args:
        verb (Annotated[VerbQuery, Depends): _description_
        session (Annotated[AsyncSession, Depends): _description_

    Returns:
        NegativeFormResponse: _description_
    """
    origin = verb.origin

    # Fill the None filed of the post query
    # Create the negative form if not specifying
    if verb.negative:
        negative = verb.negative
    else:
        # Specifying the LLM
        model = GeminiModel(settings.AI_model, api_key=settings.gemini_api_key)
        # Initialize the korean verb handler
        korean_verb_handler = KoreanVerbHandler(model)
        negative = await korean_verb_handler.to_negative(verb.origin)

    # Create the audio if not specifying
    if verb.audio:
        audio = verb.audio
    else:
        # Create the audio
        audio_creator = AudioCreator()
        audio = audio_creator.create_audio(negative)

    # Construct the post query
    vocabulary = PostQuery(origin=origin, variance=negative, audio=audio)

    # Build the connection to the tables
    nr = NegativeVerbRepository(
        db=session,
        main_table=KoreanVerbTable,
        variance_table=KoreanVerbVarianceNegativeTable,
    )

    # Creating a new row using the constructed post query
    try:
        result = await nr.create(vocabulary)
    except ValueError as e:
        error_msg = f"Error when adding verb '{verb.origin}'"
        raise HTTPException(status_code=404, detail=error_msg) from e

    # Construct the responses
    return NegativeFormResponse(
        origin=result.origin,
        negative=result.variance,
        audio=result.audio,
    )
