"""
User Model Classes demonstrating Inheritance and Polymorphism in Python
"""

class User:
    """Base User class for GameVault platform"""
    def __init__(self, user_id: int, username: str, email: str, country: str = "N/A", wallet_balance: float = 0.0):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.country = country
        self._wallet_balance = float(wallet_balance)

    @property
    def wallet_balance(self) -> float:
        """Encapsulated wallet balance getter"""
        return self._wallet_balance

    @wallet_balance.setter
    def wallet_balance(self, value: float):
        if value < 0:
            raise ValueError("Wallet balance cannot be negative.")
        self._wallet_balance = value

    def get_role(self) -> str:
        return "Generic User"

    def get_dashboard_options(self) -> list:
        """Polymorphic method overridden in subclasses"""
        return []

    def __str__(self):
        return f"User #{self.user_id}: {self.username} ({self.email}) - Wallet: ₹{self._wallet_balance:.2f}"


class Customer(User):
    """Customer Subclass with purchasing and library rights"""
    def get_role(self) -> str:
        return "Customer"

    def get_dashboard_options(self) -> list:
        return [
            ("1", "🎮 Browse Game Catalog & Pricing"),
            ("2", "🔍 Search Game Details"),
            ("3", "🛒 Purchase a Game"),
            ("4", "📚 My Game Library"),
            ("5", "❤️ My Wishlist"),
            ("6", "⭐ Write a Game Review"),
            ("7", "💳 View Purchase History & Total Spend"),
            ("0", "🚪 Logout")
        ]


class Admin(User):
    """Admin Subclass with platform management and analytics rights"""
    def get_role(self) -> str:
        return "Administrator"

    def get_dashboard_options(self) -> list:
        return [
            ("1", "➕ Add New Game (Auto-creates Dev/Pub)"),
            ("2", "🏷️ Apply Discount to Game"),
            ("3", "🔥 View Top Selling Games"),
            ("4", "📊 Developer Revenue Analytics"),
            ("5", "💰 Total Store Lifetime Revenue"),
            ("6", "👥 List Registered Platform Users"),
            ("0", "🚪 Logout")
        ]
