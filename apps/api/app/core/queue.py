from arq import create_pool
from app.core.redis import REDIS_SETTINGS


async def get_pool():
    return await create_pool(REDIS_SETTINGS)