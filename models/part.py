# models/part.py
class Part:
    def __init__(self, id=None, name="", category_id=None, quantity=0, price=0.0):
        self.id = id
        self.name = name
        self.category_id = category_id  # Changed from category
        self.quantity = quantity
        self.price = price

    def validate(self):
        if not self.name.strip():
            return False, "Part name cannot be empty!"
        if self.category_id is None:
            return False, "Category must be selected!"
        if self.quantity < 0:
            return False, "Quantity cannot be negative!"
        if self.price < 0:
            return False, "Price cannot be negative!"
        return True, ""