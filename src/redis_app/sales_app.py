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

    def create_hot_product_stock(self, product_id: str, count: int) -> dict:
        try:
            self.inventory_manager.set_stock(
                product_id=product_id,
                count=count,
            )

            return {
                "status": 200,
                "message": f"Stock created {product_id}:{count}"
            }

        except Exception as e:
            return {
                "status": 400,
                "message": f"Error in stock creation {product_id}:{count}. {str(e)}"
            }

    def process_purchase_request(self, user_ip: str, product_id: str) -> dict:

        try:
            print(f"\n[Incoming Request from {user_ip}]")
            allowed = self.rate_limiter.is_allowed(
                user_id=user_ip,
                limit=self.rate_limit
            )

            if not allowed:
                return {
                    "status": 429,
                    "message": "Too many requests"
                }

            purchase_result = self.buy_item(product_id=product_id)
            response = self.handle_purchase_result(
                product_id=product_id,
                result=purchase_result
            )

            return response

        except Exception as e:
            return {
                "status": 400,
                "message": f"Error in purchase request. {str(e)}"
            }

    def handle_purchase_result(self, product_id: str, result: dict) -> dict:
        if result.get("status") != 200:
            return result

        if "sold out" in result.get("message", str):
            return {
                "status": 200,
                "message": "Not enough stock"
            }

        leaderboard_result = self.update_leaderboard(product_id=product_id)
        return {
            "status": 200,
            "message": f"{result.get('message')}. {leaderboard_result.get('message')}",
        }

    def update_leaderboard(self, product_id: str) -> dict:
        try:
            self.trending_manager.record_view(product_id=product_id)
            return {
                "status": 200,
                "message": f"Leaderboard updated {product_id}"
            }

        except Exception as e:
            return {
                "status": 400,
                "message": f"Error in leaderboard update {product_id}. {str(e)}"
            }

    def buy_item(self, product_id: str) -> dict:
        try:
            result = self.inventory_manager.buy_item(
                product_id=product_id
            )
            msg = f"Item bought. {product_id}" if result == 1 else "sold out"

            return {
                "status": 200,
                "message": msg
            }

        except Exception as e:
            return {
                "status": 400,
                "message": f"Error in purchase {product_id}. {str(e)}"
            }






