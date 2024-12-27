from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from korean_verb_tool.db.base import KoreanVerbTable


async def create_korean_verb(db: AsyncSession, korean_verb: str) -> KoreanVerbTable:
    """Inserting rows to KoreanVerbTable.

    Args:
        db (AsyncSession): _description_
        korean_verb (str): _description_

    Returns:
        _type_: _description_
    """
    new_verb = KoreanVerbTable(korean_verb=korean_verb)
    db.add(new_verb)
    await db.commit()
    await db.refresh(new_verb)
    return new_verb


async def get_korean_verb_by_id(db: AsyncSession, verb_id: int) -> str:
    """Return korean verb by a given id from KoreanVerbTable.

    Args:
        db (AsyncSession): _description_
        verb_id (int): _description_

    Returns:
        _type_: _description_
    """
    # Create a select statement
    stmt = select(KoreanVerbTable).filter(KoreanVerbTable.id == verb_id)

    # Execute the query
    result = await db.execute(stmt)

    # Fetch the first matching result
    korean_verb = result.scalars().first()

    return korean_verb.korean_verb
