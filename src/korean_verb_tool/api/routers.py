from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceNegativeTable
from korean_verb_tool.db.cruds import NegativeVerbRepository
from korean_verb_tool.db.session import get_db
from korean_verb_tool.schemas.apischemas import NegativeFormResponse, VerbQuery

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
