from app.core.redis import REDIS_SETTINGS


async def first_job(ctx, message: str):
    return {"status": "successful", "message": message}


class WorkerSettings:
    functions = [first_job]
    redis_config = REDIS_SETTINGS
