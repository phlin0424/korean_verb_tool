import uuid
from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from korean_verb_tool.config import settings
from korean_verb_tool.db.base import KoreanVerbTable, KoreanVerbVarianceNegativeTable
from korean_verb_tool.utils.audio import AudioCreator
from korean_verb_tool.utils.verb_variance import generate_negative_variance


class BaseRepository(ABC):
    """Base module for executing db CRUD. (async)."""

    def __init__(self, db: AsyncSession, main_table: type[DeclarativeMeta]) -> None:
        self.db = db
        self.main_table = main_table

    @abstractmethod
    async def create() -> None:
        pass

    @abstractmethod
    async def delete() -> None:
        pass

    @abstractmethod
    async def get():
        pass

    # @abstractmethod
    # async def update():
    #     pass

    async def create_korean_verb(self, korean_verb: str) -> KoreanVerbTable:
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
        self.db.add(new_verb)
        await self.db.commit()
        await self.db.refresh(new_verb)
        return new_verb

    async def get_row_by_korean_verb(self, korean_verb: str) -> KoreanVerbTable:
        """Get the row by specifying korean verb.

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


class NegativeVerbRepository(BaseRepository):
    """Deal with negative form of korean crud."""

    def __init__(
        self,
        db: AsyncSession,
        main_table: type[DeclarativeMeta],
        variance_table: type[DeclarativeMeta],
    ) -> None:
        """Initialize the class."""
        super().__init__(db=db, main_table=main_table)
        self.variance_table = variance_table

    async def create_korean_variance(
        self,
        korean_variance: str,
        relationship_table: KoreanVerbTable,
    ) -> KoreanVerbTable:
        """Generic function to insert a row into a korean variance table.

        Args:
            korean_variance (str): _description_
            relationship_table (KoreanVerbTable): The main table row that related to the created variance row.

        Returns:
            KoreanVerbTable | KoreanVerbVarianceBaseTable: _description_
        """
        try:
            # Create the audio
            audio_creator = AudioCreator()
            mp3filename = audio_creator.create_audio(korean_variance)

            # Create a row using the predefined table model
            new_row = self.variance_table(
                korean_verb_variance_negative=korean_variance,
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

    async def create(self, korean_verb: str) -> None:
        """Insert a new korean verb into the main table and generates the corresponding variance and the audios.

        Args:
            korean_verb (str): string
        """
        # Generate verb variance using AI agent
        korean_verb_negative = await generate_negative_variance(korean_verb)

        # Insert into the main table
        main_row = await self.create_korean_verb(korean_verb=korean_verb)

        # Insert into the variance table
        await self.create_korean_variance(
            korean_variance=korean_verb_negative,
            relationship_table=main_row,
        )

    async def delete(self, korean_verb: str) -> None:
        pass

    async def get(self, korean_verb: str) -> KoreanVerbVarianceNegativeTable:
        """Get the corresponding variance row for a giving verb.

        Args:
            korean_verb (str): _description_

        Returns:
            KoreanVerbVarianceNegativeTable: _description_
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

        return fetched_row
