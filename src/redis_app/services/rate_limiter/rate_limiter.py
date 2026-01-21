from redis import Redis
import time


class RateLimiter:
    def __init__(self, client: Redis):
        self.client = client
        self._lua_script = self.__get_lua_script()
        self.script = self.client.register_script(self._lua_script)

    @staticmethod
    def __get_lua_script():
        return """
            local current = redis.call('INCR', KEYS[1])
            if current == 1 then
            redis.call('EXPIRE', KEYS[1], ARGV[1])
            end
            return current
        """
    def is_allowed(self, user_id: str, limit: int = 5, window: int = 60) -> bool:
        current_time = int(time.time() // window)
        key = f"ratelimit:{user_id}:{current_time}"

        count = self.script(keys=[key], args=[window])
        return count <= limit
