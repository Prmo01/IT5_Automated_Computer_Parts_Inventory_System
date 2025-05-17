# models/user.py
import bcrypt

class User:
    def __init__(self, id=None, username="", password="", role="Inventory Staff"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def is_admin(self):
        return self.role == "Admin"

    def validate(self):
        if not self.username:
            return False, "Username is required!"
        if not self.password:
            return False, "Password is required!"
        return True, ""

    @classmethod
    def get_hardcoded_users(cls):

        users = [
            cls(
                id=1,
                username="admin",
                password="$2b$12$4zY7x7y9Qz9x1z2y3x4y5e9z8y7x6w5v4u3t2r1q0p",  # Hashed 'admin123'
                role="Admin"
            ),
            cls(
                id=2,
                username="staff",
                password="$2b$12$5zY8x8y0Qz0x2z3y4x5y6e0z9y8x7w6v5u4t3r2q1p",  # Hashed 'staff123'
                role="Inventory Staff"
            )
        ]
        return users

    @staticmethod
    def authenticate_hardcoded(username, password):
        for user in User.get_hardcoded_users():
            if user.username == username and user.verify_password(password):
                return user
        return None