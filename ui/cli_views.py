"""
CLI Views and Terminal UI Formatting Helpers
Provides clean ASCII banners, formatted tables, and ANSI color coding.
"""

class CLIViews:
    """Terminal ASCII UI renderer with ANSI formatting"""

    # ANSI Colors
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @classmethod
    def print_banner(cls):
        print(f"{cls.CYAN}{cls.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║          🎮 GAMEVAULT ONLINE STORE & DATABASE 🎮             ║")
        print("║                   Python - MySQL System                      ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{cls.RESET}")

    @classmethod
    def print_header(cls, title: str):
        width = 62
        print(f"\n{cls.BLUE}{cls.BOLD}┌" + "─" * (width - 2) + "┐")
        print(f"│ {title:^{width - 4}} │")
        print("└" + "─" * (width - 2) + f"┘{cls.RESET}")

    @classmethod
    def print_catalog(cls, catalog: list):
        cls.print_header("🎮 GAME STORE CATALOG")
        if not catalog:
            print("No games available.")
            return

        print(f"{cls.BOLD}{'ID':<4} {'Title':<25} {'Price':<12} {'Orig Price':<12} {'Rating':<10} {'Developer':<18}{cls.RESET}")
        print("─" * 85)

        for game in catalog:
            discount_tag = f"{cls.GREEN}🔥 SALE{cls.RESET}" if game['price'] < game['original_price'] else ""
            rating_str = f"⭐ {game['rating']:.1f}" if game['rating'] > 0 else "Unrated"
            price_str = f"₹{game['price']:.2f}"
            orig_str = f"₹{game['original_price']:.2f}" if game['price'] < game['original_price'] else "-"

            print(f"{game['game_id']:<4} {game['title']:<25} {cls.GREEN if game['price'] < game['original_price'] else ''}{price_str:<12}{cls.RESET} {orig_str:<12} {rating_str:<10} {game['developer']:<18} {discount_tag}")

    @classmethod
    def print_game_details(cls, details: dict):
        if not details:
            print(f"{cls.RED}Game details not found.{cls.RESET}")
            return

        cls.print_header(f"🎮 GAME DETAILS: {details.get('Title', 'N/A')}")
        print(f"  📌 Game ID        : {details.get('GameID')}")
        print(f"  🏷️  Title          : {details.get('Title')}")
        print(f"  🏢 Developer      : {details.get('DeveloperName') or 'N/A'}")
        print(f"  📢 Publisher      : {details.get('PublisherName') or 'N/A'}")
        print(f"  🎭 Genres         : {details.get('Genres') or 'N/A'}")
        print(f"  ⭐ Average Rating : {details.get('AverageRating') or 0.0} / 5.00")
        print(f"  💰 Current Price  : ₹{details.get('CurrentPrice') or 0.00:.2f}")

    @classmethod
    def print_library(cls, library: list):
        cls.print_header("📚 MY GAME LIBRARY")
        if not library:
            print("You don't own any games yet. Visit the catalog to buy games!")
            return

        print(f"{cls.BOLD}{'Game ID':<10} {'Title':<30} {'Purchase Date':<15} {'Hours Played':<12}{cls.RESET}")
        print("─" * 70)
        for item in library:
            print(f"{item['GameID']:<10} {item['Title']:<30} {str(item['PurchaseDate']):<15} {item['HoursPlayed']:<12}")

    @classmethod
    def print_wishlist(cls, wishlist: list):
        cls.print_header("❤️ MY WISHLIST")
        if not wishlist:
            print("Your wishlist is empty.")
            return

        print(f"{cls.BOLD}{'Game ID':<10} {'Title':<30} {'Price':<12} {'Added Date':<15}{cls.RESET}")
        print("─" * 70)
        for item in wishlist:
            print(f"{item['GameID']:<10} {item['Title']:<30} ₹{float(item['Price']):<11.2f} {str(item['AddedDate']):<15}")

    @classmethod
    def print_purchase_history(cls, history: list, total_spend: float):
        cls.print_header("💳 PURCHASE HISTORY")
        if not history:
            print("No orders placed yet.")
        else:
            print(f"{cls.BOLD}{'Order ID':<10} {'Game Title':<30} {'Price Paid':<15} {'Order Date':<20}{cls.RESET}")
            print("─" * 78)
            for order in history:
                print(f"{order['OrderID']:<10} {order['Title']:<30} ₹{float(order['PurchasePrice']):<14.2f} {str(order['OrderDate']):<20}")

        print(f"\n{cls.BOLD}{cls.GREEN}💰 Total Lifetime Spend: ₹{total_spend:.2f}{cls.RESET}")

    @classmethod
    def print_top_selling(cls, top_games: list):
        cls.print_header("🔥 TOP SELLING GAMES")
        if not top_games:
            print("No sales data available.")
            return
        print(f"{cls.BOLD}{'Rank':<6} {'Game ID':<10} {'Title':<35} {'Copies Sold':<12}{cls.RESET}")
        print("─" * 65)
        for i, item in enumerate(top_games, 1):
            print(f"#{i:<5} {item['GameID']:<10} {item['Title']:<35} {item['CopiesSold']:<12}")

    @classmethod
    def print_developer_revenue(cls, dev_revenue: list):
        cls.print_header("📊 REVENUE BY DEVELOPER")
        if not dev_revenue:
            print("No revenue data available.")
            return
        print(f"{cls.BOLD}{'Dev ID':<8} {'Developer Name':<35} {'Total Revenue':<15}{cls.RESET}")
        print("─" * 60)
        for item in dev_revenue:
            print(f"{item['DeveloperID']:<8} {item['DeveloperName']:<35} ₹{float(item['TotalRevenue'] or 0.0):<14.2f}")

    @classmethod
    def print_users(cls, users: list):
        cls.print_header("👥 REGISTERED USERS")
        if not users:
            print("No users found.")
            return
        print(f"{cls.BOLD}{'ID':<4} {'Username':<18} {'Email':<25} {'Country':<12} {'Wallet':<12}{cls.RESET}")
        print("─" * 75)
        for u in users:
            print(f"{u['UserID']:<4} {u['Username']:<18} {u['Email']:<25} {u.get('Country','N/A'):<12} ₹{float(u['WalletBalance']):<11.2f}")
