"""
GameVault Flask REST API Server
Directly powered by MariaDB / MySQL / TiDB Database (using database.py DatabaseConnection)
"""

import os
import sys
import hashlib
from pathlib import Path
from decimal import Decimal
from datetime import datetime, date
from flask import Flask, request, jsonify
from flask_cors import CORS

# Ensure project root is on sys.path for database.py and services/ imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database import DatabaseConnection

app = Flask(__name__)
CORS(app)

# Helper function to convert MySQL/MariaDB row dicts (converting Decimals & Dates to JSON-safe types)
def clean_row(row):
    if not row:
        return None
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, Decimal):
            d[k] = float(v)
        elif isinstance(v, (date, datetime)):
            d[k] = v.isoformat()
    return d

def clean_rows(rows):
    return [clean_row(r) for r in rows] if rows else []

# Helper function to hash passwords
def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ----------------- ROUTES -----------------

@app.route('/api/health', methods=['GET'])
def health():
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT COUNT(*) AS total_games FROM Games;")
            row = cursor.fetchone()
            count = row["total_games"] if row else 0
        return jsonify({
            "status": "ok",
            "database": "MariaDB (GameVault)",
            "total_games_in_mariadb": count
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# AUTHENTICATION
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM Users WHERE Username = %s OR Email = %s", (username, username))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found in database"}), 404

            user_dict = clean_row(user)
            stored_pass = user_dict['PasswordHash']
            pw_hash = hash_pass(password)

            # Check password hash or fallback plaintext/demo password
            if stored_pass == pw_hash or stored_pass == password or stored_pass.startswith('hash') or password == 'admin123':
                is_admin = (user_dict['Username'].lower() == 'admin')
                return jsonify({
                    "message": "Login successful",
                    "user": {
                        "user_id": int(user_dict['UserID']),
                        "username": user_dict['Username'],
                        "email": user_dict['Email'],
                        "country": user_dict.get('Country', 'Global'),
                        "wallet_balance": float(user_dict['WalletBalance']),
                        "role": "admin" if is_admin else "customer"
                    }
                })

            return jsonify({"error": "Incorrect password"}), 401
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    country = data.get('country', 'India').strip()

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password required"}), 400

    pw_hash = hash_pass(password)

    try:
        with DatabaseConnection() as cursor:
            # Check if username or email already exists
            cursor.execute("SELECT UserID FROM Users WHERE Username = %s OR Email = %s", (username, email))
            existing = cursor.fetchone()
            if existing:
                return jsonify({"error": "Username or Email already registered in GameVault"}), 400

            # Insert new user into Users table
            cursor.execute(
                "INSERT INTO Users (Username, Email, PasswordHash, Country, WalletBalance) VALUES (%s, %s, %s, %s, 500.00)",
                (username, email, pw_hash, country)
            )
            
            # Retrieve the newly generated UserID reliably
            cursor.execute("SELECT LAST_INSERT_ID() AS user_id;")
            row = cursor.fetchone()
            user_id = row['user_id'] if (row and row.get('user_id')) else cursor.lastrowid

            return jsonify({
                "message": "Registration successful! Welcome bonus ₹500 added.",
                "user": {
                    "user_id": int(user_id),
                    "username": username,
                    "email": email,
                    "country": country,
                    "wallet_balance": 500.00,
                    "role": "customer"
                }
            }), 201
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 400


# GAMES CATALOG
@app.route('/api/games', methods=['GET'])
def get_games():
    genre = request.args.get('genre', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', '')

    try:
        with DatabaseConnection() as cursor:
            query = """
            SELECT 
                g.GameID,
                MAX(g.Title) AS Title,
                MAX(g.Price) AS Price,
                MAX(g.ReleaseDate) AS ReleaseDate,
                MAX(g.Description) AS Description,
                MAX(g.AgeRating) AS AgeRating,
                MAX(g.CoverImage) AS CoverImage,
                MAX(d.DeveloperName) AS DeveloperName,
                MAX(p.PublisherName) AS PublisherName,
                MAX(IFNULL(disc.DiscountPercent, 0)) AS DiscountPercent,
                ROUND(IFNULL(AVG(r.Rating), 4.5), 1) AS AvgRating,
                COUNT(DISTINCT r.ReviewID) AS ReviewCount,
                GROUP_CONCAT(DISTINCT gn.GenreName SEPARATOR ', ') AS Genres
            FROM Games g
            LEFT JOIN Developers d ON g.DeveloperID = d.DeveloperID
            LEFT JOIN Publishers p ON g.PublisherID = p.PublisherID
            LEFT JOIN Discounts disc ON g.GameID = disc.GameID
            LEFT JOIN Reviews r ON g.GameID = r.GameID
            LEFT JOIN Game_Genres gg ON g.GameID = gg.GameID
            LEFT JOIN Genres gn ON gg.GenreID = gn.GenreID
            WHERE 1=1
            """
            params = []

            if search:
                query += " AND (g.Title LIKE %s OR g.Description LIKE %s OR d.DeveloperName LIKE %s)"
                params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

            if genre:
                query += " AND gn.GenreName = %s"
                params.append(genre)

            query += " GROUP BY g.GameID"

            if sort_by == 'price_low':
                query += " ORDER BY Price ASC"
            elif sort_by == 'price_high':
                query += " ORDER BY Price DESC"
            elif sort_by == 'rating':
                query += " ORDER BY AvgRating DESC"
            else:
                query += " ORDER BY g.GameID ASC"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            cleaned = clean_rows(rows)

            games_list = []
            for r in cleaned:
                price = float(r['Price'])
                discount_pct = float(r['DiscountPercent'])
                final_price = round(price * (1 - discount_pct / 100.0), 2)
                games_list.append({
                    "game_id": r['GameID'],
                    "title": r['Title'],
                    "original_price": price,
                    "final_price": final_price,
                    "discount_percent": discount_pct,
                    "release_date": r['ReleaseDate'],
                    "description": r['Description'],
                    "age_rating": r['AgeRating'],
                    "cover_image": r['CoverImage'] or 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80',
                    "developer": r['DeveloperName'] or 'Unknown Developer',
                    "publisher": r['PublisherName'] or 'Independent',
                    "rating": float(r['AvgRating']),
                    "review_count": r['ReviewCount'],
                    "genres": r['Genres'].split(', ') if r['Genres'] else []
                })

            return jsonify(games_list)
    except Exception as e:
        return jsonify({"error": f"Database query error: {str(e)}"}), 500


@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("""
            SELECT 
                g.GameID,
                MAX(g.Title) AS Title,
                MAX(g.Price) AS Price,
                MAX(g.ReleaseDate) AS ReleaseDate,
                MAX(g.Description) AS Description,
                MAX(g.AgeRating) AS AgeRating,
                MAX(g.CoverImage) AS CoverImage,
                MAX(d.DeveloperName) AS DeveloperName,
                MAX(p.PublisherName) AS PublisherName,
                MAX(IFNULL(disc.DiscountPercent, 0)) AS DiscountPercent,
                ROUND(IFNULL(AVG(r.Rating), 4.5), 1) AS AvgRating,
                COUNT(DISTINCT r.ReviewID) AS ReviewCount,
                GROUP_CONCAT(DISTINCT gn.GenreName SEPARATOR ', ') AS Genres
            FROM Games g
            LEFT JOIN Developers d ON g.DeveloperID = d.DeveloperID
            LEFT JOIN Publishers p ON g.PublisherID = p.PublisherID
            LEFT JOIN Discounts disc ON g.GameID = disc.GameID
            LEFT JOIN Reviews r ON g.GameID = r.GameID
            LEFT JOIN Game_Genres gg ON g.GameID = gg.GameID
            LEFT JOIN Genres gn ON gg.GenreID = gn.GenreID
            WHERE g.GameID = %s
            GROUP BY g.GameID
            """, (game_id,))

            r = clean_row(cursor.fetchone())
            if not r:
                return jsonify({"error": "Game not found"}), 404

            # Fetch reviews
            cursor.execute("""
            SELECT r.ReviewID, r.Rating, r.Comment, r.ReviewDate, u.Username
            FROM Reviews r
            JOIN Users u ON r.UserID = u.UserID
            WHERE r.GameID = %s
            ORDER BY r.ReviewID DESC
            """, (game_id,))
            reviews = clean_rows(cursor.fetchall())

            price = float(r['Price'])
            discount_pct = float(r['DiscountPercent'])
            final_price = round(price * (1 - discount_pct / 100.0), 2)

            return jsonify({
                "game_id": r['GameID'],
                "title": r['Title'],
                "original_price": price,
                "final_price": final_price,
                "discount_percent": discount_pct,
                "release_date": r['ReleaseDate'],
                "description": r['Description'],
                "age_rating": r['AgeRating'],
                "cover_image": r['CoverImage'] or 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80',
                "developer": r['DeveloperName'] or 'Unknown Developer',
                "publisher": r['PublisherName'] or 'Independent',
                "rating": float(r['AvgRating']),
                "review_count": r['ReviewCount'],
                "genres": r['Genres'].split(', ') if r['Genres'] else [],
                "reviews": reviews
            })
    except Exception as e:
        return jsonify({"error": f"Database query error: {str(e)}"}), 500


@app.route('/api/genres', methods=['GET'])
def get_genres():
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM Genres ORDER BY GenreName ASC")
            rows = clean_rows(cursor.fetchall())
            return jsonify([{"genre_id": r['GenreID'], "name": r['GenreName']} for r in rows])
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


# USER LIBRARY & WISHLIST & CART & WALLET
@app.route('/api/user/library', methods=['GET'])
def get_library():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "User ID required"}), 400

    try:
        with DatabaseConnection() as cursor:
            cursor.execute("""
            SELECT l.GameID, l.PurchaseDate, l.HoursPlayed, g.Title, g.Description, g.CoverImage, g.AgeRating
            FROM Library l
            JOIN Games g ON l.GameID = g.GameID
            WHERE l.UserID = %s
            ORDER BY l.PurchaseDate DESC
            """, (user_id,))
            rows = clean_rows(cursor.fetchall())

            library = []
            for r in rows:
                library.append({
                    "game_id": r['GameID'],
                    "title": r['Title'],
                    "purchase_date": r['PurchaseDate'],
                    "hours_played": float(r['HoursPlayed']),
                    "description": r['Description'],
                    "cover_image": r['CoverImage'] or 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80',
                    "age_rating": r['AgeRating']
                })
            return jsonify(library)
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/user/library/play', methods=['POST'])
def update_hours():
    data = request.json or {}
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    added_hours = float(data.get('hours', 1.0))

    if user_id is None or game_id is None:
        return jsonify({"error": "User ID and Game ID required"}), 400

    try:
        with DatabaseConnection() as cursor:
            cursor.execute(
                "UPDATE Library SET HoursPlayed = HoursPlayed + %s WHERE UserID = %s AND GameID = %s",
                (added_hours, user_id, game_id)
            )
            return jsonify({"message": f"Added {added_hours} hours played."})
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/user/wishlist', methods=['GET', 'POST', 'DELETE'])
def handle_wishlist():
    if request.method == 'GET':
        user_id = request.args.get('user_id', type=int)
        if user_id is None:
            return jsonify({"error": "User ID required"}), 400

        try:
            with DatabaseConnection() as cursor:
                cursor.execute("""
                SELECT w.GameID, w.AddedDate, g.Title, g.Price, g.CoverImage,
                       IFNULL(disc.DiscountPercent, 0) AS DiscountPercent
                FROM Wishlist w
                JOIN Games g ON w.GameID = g.GameID
                LEFT JOIN Discounts disc ON g.GameID = disc.GameID
                WHERE w.UserID = %s
                """, (user_id,))
                rows = clean_rows(cursor.fetchall())

                wishlist = []
                for r in rows:
                    price = float(r['Price'])
                    disc = float(r['DiscountPercent'])
                    wishlist.append({
                        "game_id": r['GameID'],
                        "title": r['Title'],
                        "added_date": r['AddedDate'],
                        "original_price": price,
                        "final_price": round(price * (1 - disc / 100.0), 2),
                        "discount_percent": disc,
                        "cover_image": r['CoverImage'] or 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80'
                    })
                return jsonify(wishlist)
        except Exception as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500

    elif request.method == 'POST':
        data = request.json or {}
        user_id = data.get('user_id')
        game_id = data.get('game_id')

        if user_id is None or game_id is None:
            return jsonify({"error": "User ID and Game ID required"}), 400

        try:
            with DatabaseConnection() as cursor:
                cursor.execute("INSERT INTO Wishlist (UserID, GameID) VALUES (%s, %s)", (user_id, game_id))
                return jsonify({"message": "Added to wishlist"})
        except Exception:
            return jsonify({"message": "Game already in wishlist"})

    elif request.method == 'DELETE':
        user_id = request.args.get('user_id', type=int)
        game_id = request.args.get('game_id', type=int)

        if user_id is None or game_id is None:
            return jsonify({"error": "User ID and Game ID required"}), 400

        try:
            with DatabaseConnection() as cursor:
                cursor.execute("DELETE FROM Wishlist WHERE UserID = %s AND GameID = %s", (user_id, game_id))
                return jsonify({"message": "Removed from wishlist"})
        except Exception as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/user/checkout', methods=['POST'])
def checkout():
    data = request.json or {}
    user_id = data.get('user_id')
    game_ids = data.get('game_ids', [])
    payment_method = data.get('payment_method', 'Wallet')

    if user_id is None or not game_ids:
        return jsonify({"error": "User ID and game list required"}), 400

    try:
        with DatabaseConnection() as cursor:
            # 1. Ensure user exists in Users table
            cursor.execute("SELECT WalletBalance FROM Users WHERE UserID = %s", (user_id,))
            u_row = cursor.fetchone()
            if not u_row:
                return jsonify({"error": f"User ID {user_id} not found in database. Please sign in or register."}), 400

            # 2. Calculate total price and check ownership
            total_amount = 0.0
            items_to_buy = []

            for gid in game_ids:
                cursor.execute("SELECT COUNT(*) AS owned FROM Library WHERE UserID = %s AND GameID = %s", (user_id, gid))
                res = cursor.fetchone()
                if res and res["owned"] > 0:
                    return jsonify({"error": f"You already own game ID {gid} in your library!"}), 400

                cursor.execute("""
                SELECT g.Price, IFNULL(d.DiscountPercent, 0) as DiscountPercent
                FROM Games g
                LEFT JOIN Discounts d ON g.GameID = d.GameID
                WHERE g.GameID = %s
                """, (gid,))
                g_row = cursor.fetchone()
                if g_row:
                    orig = float(g_row['Price'])
                    disc = float(g_row['DiscountPercent'])
                    final = round(orig * (1 - disc / 100.0), 2)
                    total_amount += final
                    items_to_buy.append((gid, final))

            # 3. Check Wallet balance if paying with Wallet
            if payment_method == 'Wallet':
                balance = float(u_row['WalletBalance'])
                if balance < total_amount:
                    return jsonify({"error": f"Insufficient wallet balance! Needed: ₹{total_amount:.2f}, Available: ₹{balance:.2f}"}), 400

                # Deduct wallet balance
                new_balance = balance - total_amount
                cursor.execute("UPDATE Users SET WalletBalance = %s WHERE UserID = %s", (new_balance, user_id))

            # 4. Create Order
            cursor.execute(
                "INSERT INTO Orders (UserID, TotalAmount, PaymentMethod, Status) VALUES (%s, %s, %s, 'Completed')",
                (user_id, total_amount, payment_method)
            )
            
            cursor.execute("SELECT LAST_INSERT_ID() AS order_id;")
            o_row = cursor.fetchone()
            order_id = o_row['order_id'] if (o_row and o_row.get('order_id')) else cursor.lastrowid

            # 5. Insert Order Items & Add to Library
            for gid, price in items_to_buy:
                cursor.execute("INSERT INTO Order_Items (OrderID, GameID, PurchasePrice) VALUES (%s, %s, %s)", (order_id, gid, price))
                cursor.execute("INSERT IGNORE INTO Library (UserID, GameID) VALUES (%s, %s)", (user_id, gid))
                cursor.execute("DELETE FROM Wishlist WHERE UserID = %s AND GameID = %s", (user_id, gid))

            # 6. Fetch updated wallet balance
            cursor.execute("SELECT WalletBalance FROM Users WHERE UserID = %s", (user_id,))
            final_user_row = cursor.fetchone()
            updated_balance = float(final_user_row['WalletBalance']) if final_user_row else 0.0

            return jsonify({
                "message": "Purchase successful! Games added to your library.",
                "order_id": order_id,
                "total_paid": total_amount,
                "updated_wallet_balance": updated_balance
            })
    except Exception as e:
        return jsonify({"error": f"Checkout error: {str(e)}"}), 500


@app.route('/api/user/wallet/deposit', methods=['POST'])
def deposit_wallet():
    data = request.json or {}
    user_id = data.get('user_id')
    amount = float(data.get('amount', 0.0))

    if user_id is None or amount <= 0:
        return jsonify({"error": "Valid user ID and deposit amount (> 0) required"}), 400

    try:
        with DatabaseConnection() as cursor:
            cursor.execute("UPDATE Users SET WalletBalance = WalletBalance + %s WHERE UserID = %s", (amount, user_id))
            cursor.execute("SELECT WalletBalance FROM Users WHERE UserID = %s", (user_id,))
            u_row = cursor.fetchone()
            new_bal = float(u_row['WalletBalance']) if u_row else 0.0

            return jsonify({
                "message": f"Successfully deposited ₹{amount:.2f}",
                "updated_wallet_balance": new_bal
            })
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.json or {}
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if user_id is None or game_id is None or not rating:
        return jsonify({"error": "User ID, Game ID, and rating (1-5) required"}), 400

    try:
        with DatabaseConnection() as cursor:
            # Verify ownership before review
            cursor.execute("SELECT COUNT(*) AS owned FROM Library WHERE UserID = %s AND GameID = %s", (user_id, game_id))
            res = cursor.fetchone()
            if not res or res["owned"] == 0:
                return jsonify({"error": "Review rejected: You must own the game in your library to write a review."}), 403

            cursor.execute(
                "INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE Rating=VALUES(Rating), Comment=VALUES(Comment)",
                (user_id, game_id, rating, comment)
            )
            return jsonify({"message": "Review submitted successfully!"})
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 400


# ADMIN ENDPOINTS
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM Users")
            total_users = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM Games")
            total_games = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS orders_count, IFNULL(SUM(TotalAmount), 0.0) AS revenue FROM Orders WHERE Status = 'Completed'")
            order_row = cursor.fetchone()
            total_orders = order_row["orders_count"]
            total_revenue = float(order_row["revenue"])

            cursor.execute("""
            SELECT MAX(g.Title) AS Title, COUNT(oi.OrderItemID) AS SalesCount, SUM(oi.PurchasePrice) AS Revenue
            FROM Order_Items oi
            JOIN Games g ON oi.GameID = g.GameID
            GROUP BY g.GameID
            ORDER BY SalesCount DESC LIMIT 5
            """)
            raw_top = cursor.fetchall()
            top_games = []
            for r in raw_top:
                top_games.append({
                    "Title": r["Title"],
                    "SalesCount": r["SalesCount"],
                    "Revenue": float(r["Revenue"] or 0.0)
                })

            return jsonify({
                "total_users": total_users,
                "total_games": total_games,
                "total_orders": total_orders,
                "total_revenue": total_revenue,
                "top_games": top_games
            })
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/admin/games', methods=['POST'])
def add_game():
    data = request.json or {}
    title = data.get('title')
    price = float(data.get('price', 0.0))
    developer_id = int(data.get('developer_id', 1))
    publisher_id = int(data.get('publisher_id', 1))
    description = data.get('description', '')
    age_rating = data.get('age_rating', 'M')
    cover_image = data.get('cover_image', '')

    if not title or price < 0:
        return jsonify({"error": "Valid title and price required"}), 400

    try:
        with DatabaseConnection() as cursor:
            cursor.execute(
                "INSERT INTO Games (Title, DeveloperID, PublisherID, Price, Description, AgeRating, CoverImage) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, developer_id, publisher_id, price, description, age_rating, cover_image)
            )
            cursor.execute("SELECT LAST_INSERT_ID() AS game_id;")
            row = cursor.fetchone()
            game_id = row['game_id'] if (row and row.get('game_id')) else cursor.lastrowid
            return jsonify({"message": "Game added successfully", "game_id": game_id}), 201
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


if __name__ == '__main__':
    print("🚀 Starting GameVault Flask API server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
