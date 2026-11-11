from dotenv import load_dotenv
from redis.asyncio import Redis
import os
from arq.connections import RedisSettings

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))



URL = (f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

REDIS_SETTINGS = RedisSettings(host=REDIS_HOST, port=REDIS_PORT, database=REDIS_DB)

def get_redis():
    return Redis.from_url(URL, decode_responses=True)