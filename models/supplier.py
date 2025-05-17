# models/supplier.py
class Supplier:
    def __init__(self, id=None, name="", contact="", address=""):
        self.id = id
        self.name = name
        self.contact = contact
        self.address = address

    def validate(self):
        if not all([self.name, self.contact]):
            return False, "Name and Contact are required!"
        return True, ""