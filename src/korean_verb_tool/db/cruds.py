from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceBaseTable


async def create_korean_verb(db: AsyncSession, korean_verb: str):
    new_verb = KoreanVerbTable(korean_verb=korean_verb)
    db.add(new_verb)
    await db.commit()
    await db.refresh(new_verb)
    return new_verb


async def get_korean_verb_by_id(db: AsyncSession, verb_id: int):
    result = await db.execute(db.query(KoreanVerbTable).filter(KoreanVerbTable.id == verb_id))
    return result.scalars().first()
