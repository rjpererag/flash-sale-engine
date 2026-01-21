from redis import Redis


class InventoryManager:

    def __init__(self, client: Redis):

        self.client = client
        self._buy_script = self.__get_lua_script()
        self.buy_op = self.client.register_script(script=self._buy_script)
    
    @staticmethod
    def __get_lua_script() -> str:
        return """
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
       

    def set_stock(self, product_id: str, count: int):
        self.client.set(f"item:stock:{product_id}", count)

    def increase_stock(self, product_id: str, count: int):
        self.client.incr(name=f"item:stock:{product_id}", amount=count)

    def decrease_stock(self, product_id: str, count: int):
        self.client.decr(name=f"item:stock:{product_id}", amount=count)

    def buy_item(self, product_id: str):
        key =  f"item:stock:{product_id}"
        result = self.buy_op(keys=[key])
        return result