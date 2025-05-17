# models/category.py
class Category:
    def __init__(self, id=None, name="", description=""):
        self.id = id
        self.name = name
        self.description = description

    def validate(self):
        if not self.name.strip():
            return False, "Category name cannot be empty!"
        return True, ""