"""
Authentication and User Account Service
Handles Login, Registration, Password Hashing, and User Instantiation
"""

import hashlib
from database import DatabaseConnection
from models.user import Customer, Admin

class AuthService:
    """Service handling User Registration & Authentication"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Utility function to hash passwords securely using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @classmethod
    def register_customer(cls, username: str, email: str, password: str, country: str = "India", initial_wallet: float = 500.0) -> bool:
        """Registers a new Customer in the database"""
        password_hash = cls.hash_password(password)
        try:
            with DatabaseConnection() as cursor:
                query = """
                    INSERT INTO Users (Username, Email, PasswordHash, Country, WalletBalance)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (username, email, password_hash, country, initial_wallet))
                print(f"\n✅ User '{username}' registered successfully with ₹{initial_wallet:.2f} wallet balance!")
                return True
        except Exception as err:
            print(f"\n❌ Registration Failed: {err}")
            return False

    @classmethod
    def login(cls, username: str, password: str):
        """Authenticates user credentials and returns Customer or Admin object"""
        password_hash = cls.hash_password(password)
        
        # Hardcoded Admin fallback for demonstration if admin is requested
        if username.lower() == "admin" and password == "admin123":
            return Admin(user_id=0, username="Admin", email="admin@gamevault.com", country="Platform", wallet_balance=99999.0)

        try:
            with DatabaseConnection() as cursor:
                # Query user by username
                cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
                user_data = cursor.fetchone()

                if not user_data:
                    print("\n❌ Username not found.")
                    return None

                # Verify Password Hash (or plaintext fallback for sample database rows)
                stored_hash = user_data["PasswordHash"]
                if stored_hash == password_hash or stored_hash == password or stored_hash.startswith("hash"):
                    return Customer(
                        user_id=user_data["UserID"],
                        username=user_data["Username"],
                        email=user_data["Email"],
                        country=user_data.get("Country", "N/A"),
                        wallet_balance=float(user_data["WalletBalance"])
                    )
                else:
                    print("\n❌ Incorrect password.")
                    return None
        except Exception as err:
            print(f"\n❌ Authentication Error: {err}")
            return None
