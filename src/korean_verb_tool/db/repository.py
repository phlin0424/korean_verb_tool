from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta

from korean_verb_tool.db.cruds import create_korean_variance, create_korean_verb
from korean_verb_tool.utils.verb_variance import generate_negative_variance


class BaseRepository(ABC):
    """Base module for executing db CRUD. (async)"""

    def __init__(self, db: AsyncSession, main_table: type[DeclarativeMeta]) -> None:
        self.db = db
        self.main_table = main_table

    @abstractmethod
    async def create():
        pass

    # @abstractmethod
    # async def delete():
    #     pass

    # @abstractmethod
    # async def update():
    #     pass

    # @abstractmethod
    # async def get():
    #     pass


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

    async def create(self, korean_verb: str) -> None:
        """Insert a new korean verb into the main table and generates the corresponding variance and the audios.

        Args:
            korean_verb (str): string
        """
        # Generate verb variance using AI agent
        korean_verb_negative = await generate_negative_variance(korean_verb)

        # Insert into the main table
        main_row = await create_korean_verb(db=self.db, korean_verb=korean_verb)

        # Insert into the variance table
        await create_korean_variance(
            db=self.db,
            table_model=self.variance_table,
            korean_variance=korean_verb_negative,
            relationship_table=main_row,
        )

    # async def delete():
    #     pass
