from flask import Flask
from flask import jsonify

from .sales_app import SalesApp



app = Flask(__name__)
sales_app = SalesApp()


@app.route('/whoami', methods=['GET'])
def whoami():
    return {"status": "Hello World"}


@app.route('/get-health', methods=['GET'])
def get_health() -> dict:
    try:
        health, status = sales_app.health_checker.check()
        return health

    except Exception as e:
        return {
            "status": f"failed: {str(e)}"
        }

@app.route('/create-stock/<string:product_id>/<int:count>', methods=['POST'])
def create_stock(product_id: str, count: int) -> dict:
    response = sales_app.create_hot_product_stock(product_id=product_id, count=count)
    msg = "Product not created" if "error" in response["message"].lower() else response["message"]
    return {
        "product_id": product_id,
        **response,
        "message": msg
    }

@app.route('/buy-item/<string:product_id>', methods=['POST'])
def buy_item(product_id: str) -> dict:
    response = sales_app.buy_item(product_id=product_id)
    msg = "Product not found" if "error" in response["message"].lower() else response["message"]
    return {
        "product_id": product_id,
        **response,
        "message": msg
    }

@app.route('/increase-inventory/<string:product_id>/<int:quantity>', methods=['POST'])
def increase_inventory(product_id: str, quantity: int) -> dict:
    sales_app.inventory_manager.increase_stock(product_id=product_id, count=quantity)
    return {
        "product_id": product_id,
        "quantity": quantity
    }


@app.route('/decrease-inventory/<string:product_id>/<int:quantity>', methods=['POST'])
def decrease_inventory(product_id: str, quantity: int) -> dict:
    sales_app.inventory_manager.decrease_stock(product_id=product_id, count=quantity)
    return {
        "product_id": product_id,
        "quantity": quantity
    }