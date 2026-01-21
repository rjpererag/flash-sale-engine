import redis

class HealthChecker:

    def __init__(
            self,
            host='localhost',
            port=6379,
            service_name: str = "my-redis-app"
    ):

        self.redis = redis.Redis(host=host, port=port)
        self.service_name = service_name

    def check(self) -> tuple[dict, int]:
        try:
            is_active = self.redis.ping()
            return {
                "status": "healthy",
                "connected": is_active,
                "service_name": self.service_name,
            }, 200

        except redis.exceptions.ConnectionError:
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

