# models/order.py
from datetime import datetime

class Order:
    def __init__(self, id=None, supplier_id=None, items=None, order_date=None, status="Pending"):
        self.id = id
        self.supplier_id = supplier_id
        self.items = items or []  # List of {'part_id': int, 'quantity': int}
        self.order_date = order_date or datetime.now()
        self.status = status

    def validate(self):
        if not self.supplier_id:
            return False, "Supplier is required!"
        if not self.items:
            return False, "At least one item is required!"
        for item in self.items:
            if not item.get('part_id'):
                return False, "Part ID is required for all items!"
            if not isinstance(item.get('quantity'), int) or item['quantity'] <= 0:
                return False, "Quantity must be a positive integer for all items!"
        return True, ""