import uuid
from abc import ABC, abstractmethod

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.expression import func

from korean_verb_tool.config import settings
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceNegativeTable
from korean_verb_tool.schemas.models import PostQuery, QueryResponse


class BaseRepository(ABC):
    """Base module for executing db CRUD. (async)."""

    def __init__(self, db: AsyncSession, main_table: type[DeclarativeMeta]) -> None:
        self.db = db
        self.main_table = main_table
        self.error_msg = "Korean verb '{korean_verb}' does not exist."

    @abstractmethod
    async def create() -> QueryResponse:
        """`create` method to the repository."""
        return

    @abstractmethod
    async def delete() -> QueryResponse:
        """`delete` method to the repository."""
        return

    @abstractmethod
    async def get() -> QueryResponse:
        """`get` method to the repository."""
        return

    @abstractmethod
    async def update() -> QueryResponse:
        """`Update` method to the repository."""
        return

    async def create_korean_verb(self, korean_voc: PostQuery) -> KoreanVerbTable:
        """Inserting rows to KoreanVerbTable by specifying the inserting string.

        Args:
            db (AsyncSession): _description_
            korean_voc (Vocabulary): _description_

        Returns:
            _type_: _description_
        """
        # Create a table model
        new_verb = KoreanVerbTable(
            korean_verb=korean_voc.origin,
            korean_verb_uuid=uuid.uuid5(
                settings.namespace_uuid,
                korean_voc.origin,
            ),
        )
        # Update to the DB table
        self.db.add(new_verb)
        await self.db.commit()
        await self.db.refresh(new_verb)
        return new_verb

    async def get_row_by_korean_verb(self, korean_verb: str) -> KoreanVerbTable:
        """Get the row by specifying korean verb in string.

        Args:
            korean_verb (str): _description_

        Returns:
            KoreanVerbTable: _description_
        """
        # Create a select query
        stmt = select(self.main_table).filter_by(korean_verb=korean_verb)

        # Get the row according to the giving verb
        result = await self.db.execute(stmt)

        # Extract the first line of the selecting results.
        main_row = result.scalars().first()

        # Create the error message.
        if not main_row:
            raise ValueError(self.error_msg.format(korean_verb=korean_verb))

        return main_row

    async def delete_row_by_korean_verb(self, korean_verb: str) -> None:
        """Delete a row by specifying the Korean verb.

        Args:
            korean_verb (str): The Korean verb to identify the row to delete.
        """
        # Create a delete query
        stmt = delete(self.main_table).where(
            self.main_table.korean_verb == korean_verb,
        )

        # Execute the delete query
        result = await self.db.execute(stmt)

        # Commit the transaction to make the deletion persistent
        await self.db.commit()

        if result.rowcount == 0:
            raise ValueError(self.error_msg(korean_verb=korean_verb))


class NegativeVerbRepository(BaseRepository):
    """Deal with negative form of korean crud."""

    def __init__(
        self,
        db: AsyncSession,
        main_table: type[DeclarativeMeta],
        variance_table: type[DeclarativeMeta],
    ) -> None:
        """Initialize the class by specifying the db and tables it would connect to."""
        super().__init__(db=db, main_table=main_table)
        self.variance_table = variance_table

    async def create_korean_variance(
        self,
        korean_voc: PostQuery,
        relationship_table: KoreanVerbTable,
    ) -> KoreanVerbVarianceNegativeTable:
        """Generic function to insert a row into a korean variance table.

        Args:
            korean_voc (PostQuery): _description_
            relationship_table (KoreanVerbTable): The main table row that related to the created variance row.

        Returns:
            KoreanVerbTable | KoreanVerbVarianceBaseTable: _description_
        """
        try:
            # Create a row using the predefined table model
            new_row = self.variance_table(
                korean_verb_variance_negative=korean_voc.variance,
                audio=korean_voc.audio,
                verb=relationship_table,
            )
            self.db.add(new_row)
            await self.db.commit()
            await self.db.refresh(new_row)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

        # Return the created table model, which is row has been inserted.
        return new_row

    async def create(self, korean_voc: PostQuery) -> QueryResponse:
        """Insert a new korean verb into the main table and generates the corresponding variance and the audios.

        Args:
            korean_voc (PostQuery): vocabulary model to input.
        """
        # Insert into the main table
        main_row = await self.create_korean_verb(korean_voc=korean_voc)

        # Insert into the variance table
        variance_row = await self.create_korean_variance(
            korean_voc=korean_voc,
            relationship_table=main_row,
        )
        return QueryResponse(
            origin=main_row.korean_verb,
            audio=variance_row.audio,
            variance=variance_row.korean_verb_variance_negative,
        )

    async def update(self, korean_new_row: KoreanVerbVarianceNegativeTable) -> QueryResponse:
        """Update the existing row.

        Args:
            korean_new_row (KoreanVerbVarianceNegativeTable): _description_
        """
        # Locate the korean verb user wants to update by fetching the uuid
        # get the uuid from the main verb table
        korean_verb_uuid = korean_new_row.korean_verb_uuid

        # Construct the update statement
        stmt = (
            update(self.variance_table)
            .where(self.variance_table.korean_verb_uuid == korean_verb_uuid)
            .values(
                audio=korean_new_row.audio,
                korean_verb_variance_negative=korean_new_row.korean_verb_variance_negative,
            )
        )
        # Execute the update query
        result = await self.db.execute(stmt)

        # Commit the changes
        await self.db.commit()

        if result.rowcount == 0:
            raise ValueError(self.error_msg(korean_verb=korean_new_row.korean_verb_uuid))

        return QueryResponse(
            origin=korean_new_row.korean_verb_variance_negative,
            audio=korean_new_row.korean_verb_uuid,
            variance=korean_new_row.korean_verb_variance_negative,
        )

    async def delete(self, korean_verb: str) -> None:
        """Delete neither the verb in the main table nor the verb in the variance table.

        Args:
            korean_verb (str): _description_
        """
        # get the uuid from the main verb table
        row_main_tale = await self.get_row_by_korean_verb(korean_verb=korean_verb)
        korean_verb_uuid = row_main_tale.korean_verb_uuid

        # Create a delete query using the uuid
        stmt = delete(self.variance_table).where(
            self.variance_table.korean_verb_uuid == korean_verb_uuid,
        )
        # Execute the delete query
        result = await self.db.execute(stmt)

        # Commit the transaction to make the deletion persistent
        await self.db.commit()

        # Delete the corresponding row in the main table either:
        await self.delete_row_by_korean_verb(korean_verb)

        if result.rowcount == 0:
            raise ValueError(self.error_msg(korean_verb=korean_verb))

    async def get(self, korean_verb: str) -> QueryResponse:
        """Get the corresponding variance row for a giving verb in string.

        Args:
            korean_verb (str): The korean verb in original form.

        Returns:
            KoreanVerbVarianceNegativeTable: The returned row of the variance table. which contains the audio path.
        """
        # get the uuid from the main verb table
        row_main_tale = await self.get_row_by_korean_verb(korean_verb=korean_verb)
        korean_verb_uuid = row_main_tale.korean_verb_uuid

        # get the variance according to the uuid
        stmt2 = select(
            self.variance_table,
        ).filter_by(korean_verb_uuid=korean_verb_uuid)
        result2 = await self.db.execute(stmt2)

        # Get the variance
        fetched_row = result2.scalars().first()

        if not fetched_row:
            raise ValueError(self.error_msg.format(korean_verb=korean_verb))

        return QueryResponse(
            origin=korean_verb,
            variance=fetched_row.korean_verb_variance_negative,
            audio=fetched_row.audio,
        )

    async def get_random_row(self) -> QueryResponse:
        """Get a random row.

        Args:
            sel (_type_): _description_

        Returns:
            KoreanVerbVarianceNegativeTable: _description_
        """
        # Get a random row from main table
        stmt = select(self.main_table).order_by(func.random()).limit(1)
        result = await self.db.execute(stmt)
        fetched_row = result.scalars().first()

        # Extract the verb from the query result
        original_verb = fetched_row.korean_verb

        # Extract the uuid from the query result
        korean_verb_uuid = fetched_row.korean_verb_uuid

        # Select the variance table using the uuid
        stmt2 = select(
            self.variance_table,
        ).filter_by(korean_verb_uuid=korean_verb_uuid)
        result2 = await self.db.execute(stmt2)

        # Get the variance
        fetched_row2 = result2.scalars().first()

        return QueryResponse(
            origin=original_verb,
            variance=fetched_row2.korean_verb_variance_negative,
            audio=fetched_row2.audio,
        )
