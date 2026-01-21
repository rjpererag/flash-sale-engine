from redis import Redis


class TrendingManager:
    def __init__(
            self,
            client: Redis,
            leaderboard_key: str = "products:trending"
    ):

        self.client = client
        self.leaderboard_key = leaderboard_key

    def record_view(self, product_id: str):
        self.client.zincrby(self.leaderboard_key, 1, product_id)

    def get_top_trending(self, n: int = 5):
        return self.client.zrevrange(self.leaderboard_key, 0, n - 1, withscores=True)

    def reset_trending(self):
        self.client.delete(self.leaderboard_key)