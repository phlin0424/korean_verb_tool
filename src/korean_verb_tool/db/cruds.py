import uuid
from abc import ABC, abstractmethod

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from korean_verb_tool.config import settings
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceBaseTable, KoreanVerbVarianceNegativeTable
from korean_verb_tool.schemas.vocabulary import Vocabulary
from korean_verb_tool.utils.audio import AudioCreator


class BaseRepository(ABC):
    """Base module for executing db CRUD. (async)."""

    def __init__(self, db: AsyncSession, main_table: type[DeclarativeMeta]) -> None:
        self.db = db
        self.main_table = main_table

    @abstractmethod
    async def create() -> KoreanVerbVarianceBaseTable:
        pass

    @abstractmethod
    async def delete() -> None:
        pass

    @abstractmethod
    async def get() -> KoreanVerbVarianceBaseTable:
        pass

    # @abstractmethod
    # async def update() -> KoreanVerbVarianceBaseTable:
    #     pass

    async def create_korean_verb(self, korean_voc: Vocabulary) -> KoreanVerbTable:
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

        main_row = result.scalars().first()

        if not main_row:
            raise ValueError(f"Korean verb '{korean_verb}' does not exist.")

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
            raise ValueError(f"No row found for Korean verb '{korean_verb}'.")


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
        korean_voc: Vocabulary,
        relationship_table: KoreanVerbTable,
    ) -> KoreanVerbTable:
        """Generic function to insert a row into a korean variance table.

        Args:
            korean_voc (Vocabulary): _description_
            relationship_table (KoreanVerbTable): The main table row that related to the created variance row.

        Returns:
            KoreanVerbTable | KoreanVerbVarianceBaseTable: _description_
        """
        try:
            # Create the audio
            audio_creator = AudioCreator()
            mp3filename = audio_creator.create_audio(korean_voc.negative)

            # Create a row using the predefined table model
            new_row = self.variance_table(
                korean_verb_variance_negative=korean_voc.negative,
                audio=str(mp3filename.name),
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

    async def create(self, korean_voc: Vocabulary) -> None:
        """Insert a new korean verb into the main table and generates the corresponding variance and the audios.

        Args:
            korean_voc (Vocabulary): vocabulary model to input.
        """
        # Insert into the main table
        main_row = await self.create_korean_verb(korean_voc=korean_voc)

        # Insert into the variance table
        await self.create_korean_variance(
            korean_voc=korean_voc,
            relationship_table=main_row,
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
            raise ValueError(f"No row found for Korean verb '{korean_verb}'.")

    async def get(self, korean_verb: str) -> KoreanVerbVarianceNegativeTable:
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

        if result2.rowcount == 0:
            raise ValueError(f"No row found for Korean verb '{korean_verb}'.")

        return fetched_row
