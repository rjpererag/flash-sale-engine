import redis
from dataclasses import asdict

from .redis_settings import RedisCredentials

class RedisClient:

    def __init__(self, credentials: RedisCredentials):
        self.credentials = asdict(credentials)
        self.pool = self._get_pool()

        self.client = redis.Redis(connection_pool=self.pool)

    def _get_pool(self):
        return redis.ConnectionPool(**self.credentials)