from redis.exceptions import ConnectionError
from redis import Redis

class HealthChecker:

    def __init__(
            self,
            client: Redis,
            service_name: str = "my-redis-app"
    ):
        self.client = client
        self.service_name = service_name

    def check(self) -> tuple[dict, int]:
        try:
            is_active = self.client.ping()
            return {
                "status": "healthy",
                "connected": is_active,
                "service_name": self.service_name,
            }, 200

        except ConnectionError:
            return {
                "status": "unhealthy",
                "connected": False,
                "error": "Conenction Error",
                "service_name": self.service_name,
            }, 500

        except Exception as e:
            return {
                "status": "unhealthy",
                "connected": False,
                "error": f"{str(e)}",
                "service_name": self.service_name,
            }, 500
