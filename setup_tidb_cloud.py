"""
Script to create tables and seed TiDB Cloud database
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from database import DatabaseConnection

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Country VARCHAR(50),
    JoinDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    WalletBalance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT chk_wallet_balance CHECK (WalletBalance >= 0)
);

CREATE TABLE IF NOT EXISTS Developers (
    DeveloperID INT PRIMARY KEY AUTO_INCREMENT,
    DeveloperName VARCHAR(100) NOT NULL,
    Country VARCHAR(50),
    FoundedYear SMALLINT,
    Website VARCHAR(150),
    CONSTRAINT chk_founded_year CHECK (FoundedYear >= 1900)
);

CREATE TABLE IF NOT EXISTS Publishers (
    PublisherID INT PRIMARY KEY AUTO_INCREMENT,
    PublisherName VARCHAR(100) NOT NULL,
    Country VARCHAR(50),
    Website VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS Games (
    GameID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(150) NOT NULL,
    DeveloperID INT NOT NULL,
    PublisherID INT,
    Price DECIMAL(10,2) NOT NULL,
    ReleaseDate DATE,
    Description TEXT,
    AgeRating VARCHAR(10),
    CoverImage VARCHAR(500),
    CONSTRAINT chk_price CHECK (Price >= 0),
    CONSTRAINT fk_game_developer FOREIGN KEY(DeveloperID) REFERENCES Developers(DeveloperID) ON DELETE RESTRICT,
    CONSTRAINT fk_game_publisher FOREIGN KEY(PublisherID) REFERENCES Publishers(PublisherID) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Genres (
    GenreID INT PRIMARY KEY AUTO_INCREMENT,
    GenreName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Game_Genres (
    GameID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (GameID, GenreID),
    CONSTRAINT fk_gg_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE,
    CONSTRAINT fk_gg_genre FOREIGN KEY(GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    OrderDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PaymentMethod VARCHAR(30) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    CONSTRAINT chk_total_amount CHECK (TotalAmount >= 0),
    CONSTRAINT fk_order_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Order_Items (
    OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    GameID INT NOT NULL,
    PurchasePrice DECIMAL(10,2) NOT NULL,
    CONSTRAINT chk_purchase_price CHECK (PurchasePrice >= 0),
    CONSTRAINT uq_order_game UNIQUE(OrderID, GameID),
    CONSTRAINT fk_oi_order FOREIGN KEY(OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_oi_games FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Library (
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    PurchaseDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    HoursPlayed DECIMAL(6,1) NOT NULL DEFAULT 0,
    PRIMARY KEY(UserID, GameID),
    CONSTRAINT chk_hours_played CHECK (HoursPlayed >= 0),
    CONSTRAINT fk_lib_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_lib_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Wishlist (
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    AddedDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    PRIMARY KEY(UserID, GameID),
    CONSTRAINT fk_wl_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_wl_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reviews (
    ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    Rating TINYINT NOT NULL,
    Comment TEXT,
    ReviewDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT uq_user_game_review UNIQUE(UserID, GameID),
    CONSTRAINT chk_rating CHECK (Rating BETWEEN 1 AND 5),
    CONSTRAINT fk_rev_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_rev_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Discounts (
    DiscountID INT PRIMARY KEY AUTO_INCREMENT,
    GameID INT NOT NULL,
    DiscountPercent DECIMAL(5,2) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    CONSTRAINT chk_discount_percent CHECK (DiscountPercent BETWEEN 0 AND 100),
    CONSTRAINT chk_discount_dates CHECK (EndDate >= StartDate),
    CONSTRAINT fk_disc_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);
"""

def setup_tidb():
    print("🚀 Connecting to TiDB Cloud and setting up schema...")
    with DatabaseConnection() as cursor:
        # Create Tables
        statements = [stmt.strip() for stmt in CREATE_TABLES_SQL.split(";") if stmt.strip()]
        for stmt in statements:
            cursor.execute(stmt)
        print("✅ All 12 tables created successfully in TiDB Cloud!")

        # Seed Users
        cursor.execute("INSERT IGNORE INTO Users (UserID, Username, Email, PasswordHash, Country, WalletBalance) VALUES (1, 'admin', 'admin@gamevault.com', 'admin123', 'Global', 99999.00);")
        cursor.execute("INSERT IGNORE INTO Users (UserID, Username, Email, PasswordHash, Country, WalletBalance) VALUES (2, 'arjun_92', 'arjun92@mail.com', 'hash1', 'India', 7001.00);")
        cursor.execute("INSERT IGNORE INTO Users (UserID, Username, Email, PasswordHash, Country, WalletBalance) VALUES (3, 'sara_k', 'sarak@mail.com', 'hash2', 'USA', 5000.50);")
        cursor.execute("COMMIT;")
        print("✅ Default Users (admin, arjun_92, sara_k) created in TiDB!")

if __name__ == '__main__':
    setup_tidb()