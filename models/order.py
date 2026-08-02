"""
Order and OrderItem Model Classes
"""

class OrderItem:
    """Line item in a GameVault order"""
    def __init__(self, order_item_id: int, order_id: int, game_id: int, game_title: str, purchase_price: float):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.game_id = game_id
        self.game_title = game_title
        self.purchase_price = float(purchase_price)

class Order:
    """Order transaction object"""
    def __init__(self, order_id: int, user_id: int, order_date, total_amount: float, payment_method: str, status: str = "Completed"):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = float(total_amount)
        self.payment_method = payment_method
        self.status = status
        self.items = []

    def add_item(self, item: OrderItem):
        self.items.append(item)
