import redis


class TrendingManager:
    def __init__(self, host = "localhost", port = 6379):
        self.r = redis.Redis(host=host, port=port)
        self.leaderboard_key = "products:trending"

    def record_view(self, product_id: str):
        self.r.zincrby(self.leaderboard_key, 1, product_id)

    def get_top_trending(self, n: int = 5):
        return self.r.zrevrange(self.leaderboard_key, 0, n - 1, withscores=True)

    def reset_trending(self):
        self.r.delete(self.leaderboard_key)