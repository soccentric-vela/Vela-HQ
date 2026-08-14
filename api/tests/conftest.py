import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.db.base import Base, configure_for_tests, get_engine
from app.main import create_app

TEST_DB_URL = os.environ.get(
    "VELAHQ_TEST_DATABASE_URL",
    "postgresql+asyncpg://velahq:velahq@localhost:55432/velahq_test",
)


@pytest_asyncio.fixture(autouse=True)
async def _db():
    configure_for_tests(TEST_DB_URL)
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def client():
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    from app.db.base import get_session_factory

    async with get_session_factory()() as session:
        yield session
