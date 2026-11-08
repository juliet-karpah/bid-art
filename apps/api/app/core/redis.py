from dotenv import load_dotenv
from redis.asyncio import Redis
import os
from arq.connections import RedisSettings

load_dotenv()

URL = (f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT', '6379')}/{os.getenv('REDIS_DB','0')}")

REDIS_SETTINGS = RedisSettings(host="localhost", port=6379, database=0)

def get_redis():
    return Redis.from_url(URL, decode_responses=True)