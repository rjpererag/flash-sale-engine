import redis

class InventoryManager:

    def __init__(self, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port)
        self._buy_script = """
        local stock_key = KEYS[1]
        local current_stock = redis.call('GET', stock_key)

        -- 1. Check if the product even exists
        if current_stock == nil then
            return -1
        end

        -- 2. Check if we have enough stock
        if tonumber(current_stock) > 0 then
            -- 3. Atomically subtract 1
            redis.call('DECR', stock_key)
            return 1 -- success
        else
            -- 4. Not enough stock
            return 0 -- sold out
        end
        """
        self.buy_op = self.r.register_script(self._buy_script)


    def set_stock(self, product_id: str, count: int):
        self.r.set(f"item:stock:{product_id}", count)

    def increase_stock(self, product_id: str, count: int):
        self.r.incr(name=f"item:stock:{product_id}", amount=count)

    def decrease_stock(self, product_id: str, count: int):
        self.r.decr(name=f"item:stock:{product_id}", amount=count)

    def buy_item(self, product_id: str):
        key =  f"item:stock:{product_id}"
        result = self.buy_op(keys=[key])
        return result