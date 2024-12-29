from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceBaseTable


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


async def create_row(db: AsyncSession, table_model, **kwargs) -> KoreanVerbTable | KoreanVerbVarianceBaseTable:
    """Generic function to insert a row into a table.

    Args:
        db (AsyncSession): The database session.
        table_model (_type_): The SQLAlchemy ORM table model class.
        **kwargs: Column values to be inserted as keyword arguments.

    Raises:
        e: The newly created row object.
    """
    try:
        # Create a row using the predefined table model
        new_row = table_model(**kwargs)
        db.add(new_row)
        await db.commit()
        await db.refresh(new_row)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

    # Return the created table model, which is row has been inserted.
    return new_row


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
