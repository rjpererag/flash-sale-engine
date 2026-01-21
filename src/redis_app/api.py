from flask import Flask
from flask import jsonify

from .sales_app import SalesApp
from .services import RedisCredentials



app = Flask(__name__)
sales_app = SalesApp(credentials=RedisCredentials())


@app.route('/whoami', methods=['GET'])
def whoami():
    try:
        return jsonify({"message": "Hello World"}), 200
    except:
        return jsonify({"message": "Internal error"}), 500


@app.route('/get-health', methods=['GET'])
def get_health():
    try:
        health, status = sales_app.health_checker.check()
        return jsonify(health), status

    except Exception as e:
        return jsonify({"status": f"failed: {str(e)}"}), 500

@app.route('/get-redis-settings', methods=['GET'])
def get_redis_settings():
    try:
        creds = sales_app.credentials
        return jsonify({"redis_credentials": creds}), 200

    except Exception as e:
        return jsonify({"status": f"failed: {str(e)}"}), 500

@app.route('/create-stock/<string:product_id>/<int:count>', methods=['POST'])
def create_stock(product_id: str, count: int) -> tuple:
    try:
        response, status = sales_app.create_hot_product_stock(product_id=product_id, count=count)
        msg = "Product not created" if "error" in response["message"].lower() else response["message"]
        return jsonify({
            **response,
            "product_id": product_id,
            "message": msg
        }), status

    except:
        return jsonify({
            "product_id": product_id,
            "message": "Internal error"
        }), 500

@app.route('/buy-item/<string:product_id>', methods=['POST'])
def buy_item(product_id: str) -> tuple:
    try:
        response, status = sales_app.process_purchase_request(
            user_ip="ABC",
            product_id=product_id
        )
        msg = "Product not found" if "error" in response["message"].lower() else response["message"]
        return jsonify({**response, "product_id": product_id, "message": msg}), status
    except:
        return jsonify({"message": "Internal error"}), 500

@app.route('/increase-inventory/<string:product_id>/<int:quantity>', methods=['POST'])
def increase_inventory(product_id: str, quantity: int) -> tuple:
    sales_app.inventory_manager.increase_stock(product_id=product_id, count=quantity)
    return jsonify({"product_id": product_id, "quantity": quantity}), 200


@app.route('/decrease-inventory/<string:product_id>/<int:quantity>', methods=['POST'])
def decrease_inventory(product_id: str, quantity: int) -> tuple:
    sales_app.inventory_manager.decrease_stock(product_id=product_id, count=quantity)
    return jsonify({"product_id": product_id,"quantity": quantity}), 200