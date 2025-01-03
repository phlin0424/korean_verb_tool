import uuid

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from korean_verb_tool.config import settings
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceBaseTable


async def create_korean_verb(
    db: AsyncSession,
    korean_verb: str,
) -> KoreanVerbTable:
    """Inserting rows to KoreanVerbTable.

    Args:
        db (AsyncSession): _description_
        korean_verb (str): _description_

    Returns:
        _type_: _description_
    """
    new_verb = KoreanVerbTable(
        korean_verb=korean_verb,
        korean_verb_uuid=uuid.uuid5(
            settings.namespace_uuid,
            korean_verb,
        ),
    )
    db.add(new_verb)
    await db.commit()
    await db.refresh(new_verb)
    return new_verb


async def create_korean_variance(
    db: AsyncSession,
    table_model: type[DeclarativeMeta],
    korean_variance: str,
    relationship_table: KoreanVerbTable,
) -> KoreanVerbTable:
    """Generic function to insert a row into a korean variance table.

    Args:
        db (AsyncSession): _description_
        table_model (type[DeclarativeMeta]): _description_
        korean_variance (str): _description_
        relationship_table (KoreanVerbTable): _description_

    Returns:
        KoreanVerbTable | KoreanVerbVarianceBaseTable: _description_
    """
    try:
        # Create a row using the predefined table model
        new_row = table_model(
            korean_verb_variance_negative=korean_variance,
            verb=relationship_table,
        )
        db.add(new_row)
        await db.commit()
        await db.refresh(new_row)
    except SQLAlchemyError:
        await db.rollback()
        raise

    # Return the created table model, which is row has been inserted.
    return new_row


async def get_row_by_verb(
    db: AsyncSession,
    korean_verb: str,
    table_model: KoreanVerbVarianceBaseTable,
) -> str:
    """Retrieve the variances of a Korean verb from the table.

    Args:
        db (AsyncSession): The database session.
        table_model: The SQLAlchemy ORM table model class.
        korean_verb (str): The Korean verb to look up.

    Returns:
        UUID: The UUID of the matching row, or None if not found.
    """
    # Create a select query
    stmt = select(KoreanVerbTable.korean_verb_uuid).filter_by(korean_verb=korean_verb)
    result = await db.execute(stmt)

    # Fetch the UUID from the result
    korean_verb_uuid = result.scalars().first()

    # Retrieve the variance from the uuid
    stmt2 = select(table_model.korean_verb_variance_negative).filter_by(korean_verb_uuid=korean_verb_uuid)
    result2 = await db.execute(stmt2)

    return result2.scalars().first()


# async def update_row(
#     db: AsyncSession,
#     table_model: type[DeclarativeMeta],
#     korean_verb: str,
#     **kwargs,
# ) -> type[DeclarativeMeta]:
#     """Update a row in a table by korean verb.

#     Args:
#         db (AsyncSession): The database session.
#         table_model: The SQLAlchemy ORM table model class.
#         row_id (int): The ID of the row to update.
#         **kwargs: Column values to update (as key-value pairs).

#     Returns:
#         object: The updated row object, or None if the row does not exist.
#     """
#     try:
#         # Fetch the row to be updated
#         stmt = select(table_model).filter_by(korean_verb=korean_verb)
#         result = await db.execute(stmt)
#         row = result.scalars().first()

#         if not row:
#             return None  # Row does not exist

#         # Update the fields dynamically
#         for key, value in kwargs.items():
#             if hasattr(row, key):
#                 setattr(row, key, value)
#             else:
#                 raise ValueError(f"Column '{key}' does not exist in {table_model.__name__}.")

#         # Commit the changes
#         await db.commit()
#         await db.refresh(row)  # Refresh to get the updated values
#         return row

#     except SQLAlchemyError as e:
#         await db.rollback()
#         raise e
