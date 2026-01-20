import redis
import time


class RateLimiter:
    def __init__(self, host='localhost', port=6379):
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=0,
            decode_responses=True,
            max_connections=20
        )
        self.redis = redis.Redis(connection_pool=self.pool)

        self._lua_script = """
                local current = redis.call('INCR', KEYS[1])
                if current == 1 then
                    redis.call('EXPIRE', KEYS[1], ARGV[1])
                end
                return current
                """
        self.script = self.redis.register_script(self._lua_script)

    def is_allowed(self, user_id: str, limit: int = 5, window: int = 60) -> bool:
        current_time = int(time.time() // window)
        key = f"ratelimit:{user_id}:{current_time}"

        count = self.script(keys=[key], args=[window])
        return count <= limit
