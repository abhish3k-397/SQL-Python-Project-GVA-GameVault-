"""
Main Entry Point for GameVault Terminal CLI Application
Python - MySQL Integration featuring OOP, Procedures, Functions, Views & Triggers
"""

import sys
from ui.cli_views import CLIViews
from services.auth_service import AuthService
from services.customer_service import CustomerService
from services.admin_service import AdminService
from models.user import Customer, Admin

def auth_menu():
    """Renders authentication screen (Login / Sign Up)"""
    CLIViews.print_banner()
    print("Welcome to GameVault! Please select an option:")
    print(" 1. 🔑 Login as Existing Customer")
    print(" 2. 📝 Register New Customer Account")
    print(" 3. 🛡️  Login as Admin (admin / admin123)")
    print(" 0. 🚪 Exit System")

    choice = input("\nEnter choice (0-3): ").strip()
    return choice

def customer_loop(customer: Customer):
    """Interactive control loop for logged-in Customer"""
    while True:
        print(f"\n{CLIViews.CYAN}👤 Logged in as: {customer.username} | Wallet Balance: ₹{customer.wallet_balance:.2f}{CLIViews.RESET}")
        print("─" * 60)
        for key, title in customer.get_dashboard_options():
            print(f" {key}. {title}")

        choice = input("\nEnter option: ").strip()

        if choice == "1":
            catalog = CustomerService.get_catalog()
            CLIViews.print_catalog(catalog)

        elif choice == "2":
            try:
                game_id = int(input("\nEnter Game ID to inspect: "))
                details = CustomerService.get_game_details(game_id)
                CLIViews.print_game_details(details)
            except ValueError:
                print("⚠️ Invalid Game ID entered.")

        elif choice == "3":
            try:
                game_id = int(input("\nEnter Game ID to purchase: "))
                print("Select Payment Method:")
                print(" 1. Credit Card")
                print(" 2. Debit Card")
                print(" 3. Wallet")
                print(" 4. UPI")
                print(" 5. PayPal")
                pm_choice = input("Choice (1-5): ").strip()
                pm_map = {"1": "Credit Card", "2": "Debit Card", "3": "Wallet", "4": "UPI", "5": "PayPal"}
                payment_method = pm_map.get(pm_choice, "Credit Card")

                CustomerService.purchase_game(customer.user_id, game_id, payment_method)
            except ValueError:
                print("⚠️ Invalid input.")

        elif choice == "4":
            library = CustomerService.get_user_library(customer.user_id)
            CLIViews.print_library(library)

        elif choice == "5":
            print("\n❤️ WISHLIST MENU")
            print(" 1. View My Wishlist")
            print(" 2. Add Game to Wishlist")
            sub = input("Choice (1-2): ").strip()
            if sub == "1":
                wishlist = CustomerService.get_user_wishlist(customer.user_id)
                CLIViews.print_wishlist(wishlist)
            elif sub == "2":
                try:
                    gid = int(input("Enter Game ID: "))
                    CustomerService.add_to_wishlist(customer.user_id, gid)
                except ValueError:
                    print("⚠️ Invalid Game ID.")

        elif choice == "6":
            print("\n⭐ SUBMIT GAME REVIEW")
            try:
                gid = int(input("Enter Game ID to review: "))
                rating = int(input("Rating (1 to 5): "))
                comment = input("Review Comment: ").strip()
                CustomerService.add_review(customer.user_id, gid, rating, comment)
            except ValueError:
                print("⚠️ Invalid rating or ID input.")

        elif choice == "7":
            history, total_spend = CustomerService.get_purchase_history(customer.user_id)
            CLIViews.print_purchase_history(history, total_spend)

        elif choice == "0":
            print(f"\n👋 Goodbye {customer.username}!")
            break

        else:
            print("⚠️ Invalid choice, try again.")

def admin_loop(admin: Admin):
    """Interactive control loop for logged-in Administrator"""
    while True:
        print(f"\n{CLIViews.HEADER}🛡️  ADMINISTRATOR DASHBOARD | Session: {admin.username}{CLIViews.RESET}")
        print("─" * 60)
        for key, title in admin.get_dashboard_options():
            print(f" {key}. {title}")

        choice = input("\nEnter option: ").strip()

        if choice == "1":
            print("\n➕ ADD NEW GAME")
            title = input("Game Title: ").strip()
            dev_name = input("Developer Studio Name: ").strip()
            pub_name = input("Publisher Name (or leave blank if self-published): ").strip()
            pub_name = pub_name if pub_name else None
            try:
                price = float(input("Game Price (₹): "))
                rel_date = input("Release Date (YYYY-MM-DD): ").strip()
                AdminService.add_game(title, dev_name, pub_name, price, rel_date)
            except ValueError:
                print("⚠️ Invalid price entered.")

        elif choice == "2":
            print("\n🏷️  APPLY GAME DISCOUNT")
            try:
                gid = int(input("Game ID: "))
                percent = float(input("Discount Percentage (0-100): "))
                start_date = input("Start Date (YYYY-MM-DD): ").strip()
                end_date = input("End Date (YYYY-MM-DD): ").strip()
                AdminService.apply_discount(gid, percent, start_date, end_date)
            except ValueError:
                print("⚠️ Invalid percentage or ID input.")

        elif choice == "3":
            top_games = AdminService.get_top_selling_games()
            CLIViews.print_top_selling(top_games)

        elif choice == "4":
            dev_rev = AdminService.get_revenue_by_developer()
            CLIViews.print_developer_revenue(dev_rev)

        elif choice == "5":
            store_rev = AdminService.get_total_store_revenue()
            CLIViews.print_header("💰 STORE LIFETIME REVENUE")
            print(f"\n  {CLIViews.BOLD}{CLIViews.GREEN}Total Store Lifetime Revenue: ₹{store_rev:.2f}{CLIViews.RESET}")

        elif choice == "6":
            users = AdminService.get_registered_users()
            CLIViews.print_users(users)

        elif choice == "0":
            print("\n👋 Exiting Admin Dashboard.")
            break

        else:
            print("⚠️ Invalid option.")

def main():
    while True:
        choice = auth_menu()

        if choice == "1":
            username = input("\nUsername: ").strip()
            password = input("Password: ").strip()
            user = AuthService.login(username, password)
            if isinstance(user, Customer):
                customer_loop(user)

        elif choice == "2":
            print("\n📝 REGISTER NEW ACCOUNT")
            username = input("Enter Username: ").strip()
            email = input("Enter Email: ").strip()
            password = input("Enter Password: ").strip()
            country = input("Enter Country [India]: ").strip() or "India"
            AuthService.register_customer(username, email, password, country)

        elif choice == "3":
            username = input("\nAdmin Username: ").strip()
            password = input("Admin Password: ").strip()
            user = AuthService.login(username, password)
            if isinstance(user, Admin):
                admin_loop(user)

        elif choice == "0":
            print("\nThank you for using GameVault Platform. Goodbye!")
            sys.exit(0)

        else:
            print("\n⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
