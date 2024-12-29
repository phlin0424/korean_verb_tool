from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from korean_verb_tool.config import settings

# Database setup
DATABASE_URL = settings.postgres_local_url

# Create an async engine
engine = create_async_engine(DATABASE_URL)

# Create an async session using the engine
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """Dependency for FastAPI routes. Session generator.

    Yields:
        _type_: _description_
    """
    async with AsyncSessionLocal() as session:
        yield session
