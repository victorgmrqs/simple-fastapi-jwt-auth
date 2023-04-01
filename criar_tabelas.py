import asyncio

from core.config import settings
from core.database import engine


async def create_tables() -> None:
    import models.__all_models

    async with engine.begin() as connection:
        await connection.run_sync(settings.DBBaseModel.metadata.drop_all)
        await connection.run_sync(settings.DBBaseModel.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
