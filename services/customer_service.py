"""
Customer Service Layer
Handles Store Browsing, Checkout, Library Management, Wishlists, and Reviews
"""

from database import DatabaseConnection
from models.game import Game

class CustomerService:
    """Service wrapping Customer Database Operations"""

    @staticmethod
    def get_catalog() -> list:
        """Retrieves game catalog with discounted prices and average ratings"""
        games = []
        try:
            with DatabaseConnection() as cursor:
                query = """
                    SELECT 
                        g.GameID,
                        g.Title,
                        CalculateDiscountPrice(g.GameID) AS FinalPrice,
                        g.Price AS OriginalPrice,
                        AverageRating(g.GameID) AS AvgRating,
                        d.DeveloperName,
                        p.PublisherName
                    FROM Games g
                    LEFT JOIN Developers d ON g.DeveloperID = d.DeveloperID
                    LEFT JOIN Publishers p ON g.PublisherID = p.PublisherID;
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    games.append({
                        "game_id": row["GameID"],
                        "title": row["Title"],
                        "price": float(row["FinalPrice"]),
                        "original_price": float(row["OriginalPrice"]),
                        "developer": row["DeveloperName"] or "Unknown",
                        "publisher": row["PublisherName"] or "Self-Published",
                        "rating": float(row["AvgRating"] or 0.0)
                    })
        except Exception as err:
            print(f"❌ Error fetching catalog: {err}")
        return games

    @staticmethod
    def get_game_details(game_id: int):
        """Calls Stored Procedure GetGameDetails(p_GameID)"""
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("GetGameDetails", [game_id])
                # In MySQL connector / dict cursor, stored procedures return resultsets
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                return results[0] if results else None
        except Exception as err:
            print(f"❌ Error fetching game details: {err}")
            return None

    @staticmethod
    def purchase_game(user_id: int, game_id: int, payment_method: str) -> bool:
        """Calls Stored Procedure PurchaseGame(p_UserID, p_GameID, p_PaymentMethod)"""
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("PurchaseGame", [user_id, game_id, payment_method])
                print("\n🎉 Transaction Successful! Game added to your Library.")
                return True
        except Exception as err:
            err_msg = str(err)
            if "already own" in err_msg.lower():
                print("\n🛑 Purchase Blocked: You already own this game in your Library.")
            else:
                print(f"\n❌ Purchase Failed: {err}")
            return False

    @staticmethod
    def get_user_library(user_id: int) -> list:
        """Retrieves user owned games via Stored Procedure GetUserLibrary"""
        library = []
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("GetUserLibrary", [user_id])
                for result in cursor.stored_results():
                    library.extend(result.fetchall())
        except Exception as err:
            print(f"❌ Error loading library: {err}")
        return library

    @staticmethod
    def get_user_wishlist(user_id: int) -> list:
        """Queries user wishlist"""
        wishlist = []
        try:
            with DatabaseConnection() as cursor:
                query = """
                    SELECT g.GameID, g.Title, g.Price, w.AddedDate
                    FROM Wishlist w
                    JOIN Games g ON w.GameID = g.GameID
                    WHERE w.UserID = %s;
                """
                cursor.execute(query, (user_id,))
                wishlist = cursor.fetchall()
        except Exception as err:
            print(f"❌ Error loading wishlist: {err}")
        return wishlist

    @staticmethod
    def add_to_wishlist(user_id: int, game_id: int) -> bool:
        """Adds game to user wishlist"""
        try:
            with DatabaseConnection() as cursor:
                query = "INSERT INTO Wishlist (UserID, GameID) VALUES (%s, %s)"
                cursor.execute(query, (user_id, game_id))
                print("\n❤️ Game added to your Wishlist!")
                return True
        except Exception as err:
            print(f"\n❌ Could not add to Wishlist: {err}")
            return False

    @staticmethod
    def add_review(user_id: int, game_id: int, rating: int, comment: str) -> bool:
        """Submits a game review (Triggers trg_before_review_check_library enforce ownership)"""
        try:
            with DatabaseConnection() as cursor:
                query = "INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user_id, game_id, rating, comment))
                print("\n⭐ Review submitted successfully!")
                return True
        except Exception as err:
            err_msg = str(err)
            if "must own" in err_msg.lower():
                print("\n🛑 Review Rejected: You must own the game in your library before reviewing it!")
            else:
                print(f"\n❌ Failed to submit review: {err}")
            return False

    @staticmethod
    def get_purchase_history(user_id: int) -> tuple:
        """Retrieves full purchase history and TotalSpend function result"""
        history = []
        total_spend = 0.0
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("UserPurchaseHistory", [user_id])
                for result in cursor.stored_results():
                    history.extend(result.fetchall())
                
                # Call Function TotalSpend(p_UserID)
                cursor.execute("SELECT TotalSpend(%s) AS LifetimeSpend;", (user_id,))
                res = cursor.fetchone()
                if res and res.get("LifetimeSpend"):
                    total_spend = float(res["LifetimeSpend"])
        except Exception as err:
            print(f"❌ Error loading purchase history: {err}")
        return history, total_spend
