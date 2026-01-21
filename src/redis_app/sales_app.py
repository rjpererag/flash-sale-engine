from .health_checker import HealthChecker
from .inventory_manager import InventoryManager
from .rate_limiter import RateLimiter
from .trending_manager import TrendingManager

class SalesApp:

    def __init__(self,
                 rate_limit: int = 5
                 ):
        self.inventory_manager = InventoryManager()
        self.rate_limiter = RateLimiter()
        self.trending_manager = TrendingManager()
        self.health_checker = HealthChecker(service_name="SalesAPP")

        self.rate_limit = rate_limit

    def create_hot_product_stock(self, product_id: str, count: int) -> tuple[dict, int]:
        self.inventory_manager.set_stock(
            product_id=product_id,
            count=count,
        )

        return {"message": f"Stock created {product_id}:{count}"}, 200


    def process_purchase_request(self, user_ip: str, product_id: str) -> tuple[dict, int]:
        print(f"\n[Incoming Request from {user_ip}]")
        allowed = self.rate_limiter.is_allowed(
            user_id=user_ip,
            limit=self.rate_limit
        )

        if not allowed:
            return {"message": "Too many requests"}, 429

        purchase_result, buy_status = self.buy_item(product_id=product_id)
        response, status = self.handle_purchase_result(
            product_id=product_id,
            result=purchase_result,
            status=buy_status
        )

        return response, status

    def handle_purchase_result(self, product_id: str, result: dict, status: int) -> tuple[dict, int]:
        if (status != 200) or ("sold out" in result.get("message", str)):
            return result, status

        leaderboard_result, leaderboard_status = self.update_leaderboard(product_id=product_id)
        return {
            "message": f"{result.get('message')}. {leaderboard_result.get('message')}"
        }, leaderboard_status

    def update_leaderboard(self, product_id: str) -> tuple[dict, int]:
        try:
            self.trending_manager.record_view(product_id=product_id)
            return {"message": f"Leaderboard updated {product_id}"}, 200

        except Exception as e:
            return {"message": f"Error in leaderboard update {product_id}. {str(e)}"}, 400

    def buy_item(self, product_id: str) -> tuple[dict, int]:
        try:
            result = self.inventory_manager.buy_item(
                product_id=product_id
            )

            msg = f"Item bought. {product_id}" if result == 1 else "sold out"

            return {"message": msg}, 200

        except Exception as e:
            return {"message": f"Error in purchase {product_id}. {str(e)}"}, 400






