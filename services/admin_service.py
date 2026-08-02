"""
Admin Service Layer
Handles Catalog Additions, Discounts, Analytics, and Revenue Reporting
"""

from database import DatabaseConnection

class AdminService:
    """Service wrapping Administrative Database Operations"""

    @staticmethod
    def add_game(title: str, developer_name: str, publisher_name: str, price: float, release_date: str) -> bool:
        """Calls Stored Procedure AddGame(p_Title, p_DeveloperName, p_PublisherName, p_Price, p_ReleaseDate)"""
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("AddGame", [title, developer_name, publisher_name, price, release_date])
                print(f"\n✨ Game '{title}' successfully added to catalog!")
                return True
        except Exception as err:
            print(f"\n❌ Failed to add game: {err}")
            return False

    @staticmethod
    def apply_discount(game_id: int, discount_percent: float, start_date: str, end_date: str) -> bool:
        """Calls Stored Procedure ApplyDiscount(p_GameID, p_DiscountPercent, p_StartDate, p_EndDate)"""
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("ApplyDiscount", [game_id, discount_percent, start_date, end_date])
                print(f"\n🏷️  {discount_percent}% Discount applied to Game ID {game_id} ({start_date} to {end_date})!")
                return True
        except Exception as err:
            print(f"\n❌ Failed to apply discount: {err}")
            return False

    @staticmethod
    def get_top_selling_games() -> list:
        """Calls Stored Procedure GetTopSellingGames()"""
        top_games = []
        try:
            with DatabaseConnection() as cursor:
                cursor.callproc("GetTopSellingGames", [])
                for result in cursor.stored_results():
                    top_games.extend(result.fetchall())
        except Exception as err:
            print(f"❌ Error fetching top selling games: {err}")
        return top_games

    @staticmethod
    def get_revenue_by_developer() -> list:
        """Queries View RevenueByDeveloper"""
        revenue = []
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT * FROM RevenueByDeveloper;")
                revenue = cursor.fetchall()
        except Exception as err:
            print(f"❌ Error fetching developer revenue: {err}")
        return revenue

    @staticmethod
    def get_total_store_revenue() -> float:
        """Calls SQL Function TotalRevenue()"""
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT TotalRevenue() AS StoreRevenue;")
                res = cursor.fetchone()
                return float(res["StoreRevenue"]) if res and res.get("StoreRevenue") else 0.0
        except Exception as err:
            print(f"❌ Error calculating total revenue: {err}")
            return 0.0

    @staticmethod
    def get_registered_users() -> list:
        """Queries registered platform users"""
        users = []
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT UserID, Username, Email, Country, JoinDate, WalletBalance FROM Users;")
                users = cursor.fetchall()
        except Exception as err:
            print(f"❌ Error fetching users: {err}")
        return users
