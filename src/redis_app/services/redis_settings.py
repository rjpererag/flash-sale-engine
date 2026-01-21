from decouple import config
from dataclasses import dataclass


@dataclass(frozen=True)
class RedisCredentials:
    host: str = config("REDIS_HOST", cast=str, default="localhost")
    port: int = config("REDIS_PORT", cast=int, default=6379)
    db: int = config("REDIS_DB", cast=int, default=0)
    max_connections: int = config("REDIS_MAX_CONNECTIONS", cast=int, default= 20)
    decode_responses: bool = config("REDIS_DECODE_RESPONSES", cast=bool, default=True)
