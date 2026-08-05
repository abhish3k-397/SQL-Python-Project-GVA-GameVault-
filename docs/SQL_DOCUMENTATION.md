# GameVault — Complete Database Project Documentation

**Engine target:** MySQL 8.0+ (needed for enforced `CHECK` constraints, window-function-free design keeps it compatible with 8.0.16+)

## Deliverables Summary

| Component | Count |
|---|---:|
| Tables | 12 |
| Views | 7 |
| Stored Procedures | 8 |
| Functions | 6 |
| Triggers | 7 |
| Indexes | 6 |
| Analytical Queries | 40 |
| Sample Records | Representative seed set (scalable to ~2000) |

## Suggested File Structure

```
GameVault/
├── 01_Create_Database.sql
├── 02_Create_Tables.sql
├── 03_Insert_Data.sql
├── 04_Indexes.sql
├── 05_Views.sql
├── 06_Functions.sql
├── 07_Procedures.sql
├── 08_Triggers.sql
├── 09_Queries.sql
├── ER_Diagram.pdf
├── Data_Dictionary.pdf
└── Project_Report.pdf
```

Every script below is numbered to match this file layout — copy each section into its corresponding `.sql` file, or run this document top to bottom against a fresh schema.

---

## 1. Database & Table Creation

```sql
-- 01_Create_Database.sql
DROP DATABASE IF EXISTS GameVault;
CREATE DATABASE GameVault CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE GameVault;
```

```sql
-- 02_Create_Tables.sql

CREATE TABLE Users (
    UserID          INT AUTO_INCREMENT PRIMARY KEY,
    Username        VARCHAR(50)  NOT NULL UNIQUE,
    Email           VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash    VARCHAR(255) NOT NULL,
    Country         VARCHAR(50),
    JoinDate        DATE NOT NULL DEFAULT (CURRENT_DATE),
    WalletBalance   DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT chk_wallet_balance CHECK (WalletBalance >= 0)
);

CREATE TABLE Developers (
    DeveloperID     INT AUTO_INCREMENT PRIMARY KEY,
    DeveloperName   VARCHAR(100) NOT NULL,
    Country         VARCHAR(50),
    FoundedYear     SMALLINT,
    Website         VARCHAR(150),
    CONSTRAINT chk_founded_year CHECK (FoundedYear <= YEAR(CURDATE()))
);

CREATE TABLE Publishers (
    PublisherID     INT AUTO_INCREMENT PRIMARY KEY,
    PublisherName   VARCHAR(100) NOT NULL,
    Country         VARCHAR(50),
    Website         VARCHAR(150)
);

CREATE TABLE Games (
    GameID          INT AUTO_INCREMENT PRIMARY KEY,
    Title           VARCHAR(150) NOT NULL,
    DeveloperID     INT NOT NULL,
    PublisherID     INT NULL,
    Price           DECIMAL(8,2) NOT NULL,
    ReleaseDate     DATE,
    Description     TEXT,
    AgeRating       VARCHAR(10),
    CONSTRAINT chk_price CHECK (Price >= 0),
    CONSTRAINT fk_games_developer FOREIGN KEY (DeveloperID)
        REFERENCES Developers(DeveloperID) ON DELETE RESTRICT,
    CONSTRAINT fk_games_publisher FOREIGN KEY (PublisherID)
        REFERENCES Publishers(PublisherID) ON DELETE SET NULL
);

CREATE TABLE Genres (
    GenreID         INT AUTO_INCREMENT PRIMARY KEY,
    GenreName       VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Game_Genres (
    GameID          INT NOT NULL,
    GenreID         INT NOT NULL,
    PRIMARY KEY (GameID, GenreID),
    CONSTRAINT fk_gg_game  FOREIGN KEY (GameID)  REFERENCES Games(GameID)   ON DELETE CASCADE,
    CONSTRAINT fk_gg_genre FOREIGN KEY (GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE
);

CREATE TABLE Orders (
    OrderID         INT AUTO_INCREMENT PRIMARY KEY,
    UserID          INT NOT NULL,
    OrderDate       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PaymentMethod   VARCHAR(30),
    Status          VARCHAR(20) NOT NULL DEFAULT 'Pending',
    CONSTRAINT chk_total_amount CHECK (TotalAmount >= 0),
    CONSTRAINT chk_order_status CHECK (Status IN ('Pending','Completed','Cancelled','Refunded')),
    CONSTRAINT fk_orders_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

CREATE TABLE Order_Items (
    OrderItemID     INT AUTO_INCREMENT PRIMARY KEY,
    OrderID         INT NOT NULL,
    GameID          INT NOT NULL,
    PurchasePrice   DECIMAL(8,2) NOT NULL,
    CONSTRAINT uq_order_game UNIQUE (OrderID, GameID),
    CONSTRAINT fk_oi_order FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_oi_game  FOREIGN KEY (GameID)  REFERENCES Games(GameID)   ON DELETE RESTRICT
);

CREATE TABLE Library (
    UserID          INT NOT NULL,
    GameID          INT NOT NULL,
    PurchaseDate    DATE NOT NULL,
    HoursPlayed     DECIMAL(6,1) NOT NULL DEFAULT 0,
    PRIMARY KEY (UserID, GameID),
    CONSTRAINT chk_hours_played CHECK (HoursPlayed >= 0),
    CONSTRAINT fk_lib_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_lib_game FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE Wishlist (
    UserID          INT NOT NULL,
    GameID          INT NOT NULL,
    AddedDate       DATE NOT NULL DEFAULT (CURRENT_DATE),
    PRIMARY KEY (UserID, GameID),
    CONSTRAINT fk_wl_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_wl_game FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE Reviews (
    ReviewID        INT AUTO_INCREMENT PRIMARY KEY,
    UserID          INT NOT NULL,
    GameID          INT NOT NULL,
    Rating          TINYINT NOT NULL,
    Comment         TEXT,
    ReviewDate      DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT uq_user_game_review UNIQUE (UserID, GameID),
    CONSTRAINT chk_rating CHECK (Rating BETWEEN 1 AND 5),
    CONSTRAINT fk_rev_user FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_rev_game FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

CREATE TABLE Discounts (
    DiscountID       INT AUTO_INCREMENT PRIMARY KEY,
    GameID           INT NOT NULL,
    DiscountPercent  DECIMAL(5,2) NOT NULL,
    StartDate        DATE NOT NULL,
    EndDate          DATE NOT NULL,
    CONSTRAINT chk_discount_percent CHECK (DiscountPercent BETWEEN 0 AND 100),
    CONSTRAINT chk_discount_dates CHECK (EndDate > StartDate),
    CONSTRAINT fk_disc_game FOREIGN KEY (GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);
```

**Constraints implemented:** `UNIQUE` on Username/Email/GenreName/(OrderID,GameID)/(UserID,GameID reviews); `CHECK` on Price, WalletBalance, Rating, DiscountPercent, HoursPlayed, TotalAmount, Order.Status, Discount date order; `NOT NULL` on all required fields; `FOREIGN KEY` on every relationship with `ON DELETE` rules chosen per relationship (`CASCADE` for dependent/junction data, `RESTRICT` where deleting the parent should be blocked, `SET NULL` where the child can legitimately exist without that parent).

---

## 2. Indexes

```sql
-- 04_Indexes.sql
CREATE INDEX idx_game_title      ON Games(Title);
CREATE INDEX idx_game_price      ON Games(Price);
CREATE INDEX idx_game_developer  ON Games(DeveloperID);
CREATE INDEX idx_order_date      ON Orders(OrderDate);
CREATE INDEX idx_review_rating   ON Reviews(Rating);
CREATE INDEX idx_discount_dates  ON Discounts(StartDate, EndDate);
```

*(`Username`, `Email`, and `GenreName` are already indexed automatically via their `UNIQUE` constraints, so they aren't duplicated here.)*

---

## 3. Views

```sql
-- 05_Views.sql

-- 1. Games currently on sale
CREATE VIEW CurrentDiscounts AS
SELECT
    g.GameID,
    g.Title,
    g.Price AS OriginalPrice,
    d.DiscountPercent,
    ROUND(g.Price * (1 - d.DiscountPercent / 100), 2) AS FinalPrice,
    d.StartDate,
    d.EndDate
FROM Games g
JOIN Discounts d ON g.GameID = d.GameID
WHERE CURDATE() BETWEEN d.StartDate AND d.EndDate;

-- 2. Rating summary per game
CREATE VIEW GameRatings AS
SELECT
    g.GameID,
    g.Title,
    ROUND(AVG(r.Rating), 2) AS AverageRating,
    COUNT(r.ReviewID) AS TotalReviews
FROM Games g
LEFT JOIN Reviews r ON g.GameID = r.GameID
GROUP BY g.GameID, g.Title;

-- 3. Every user's owned games
CREATE VIEW UserLibraries AS
SELECT
    u.UserID,
    u.Username,
    g.GameID,
    g.Title AS GameTitle,
    l.PurchaseDate,
    l.HoursPlayed
FROM Library l
JOIN Users u ON l.UserID = u.UserID
JOIN Games g ON l.GameID = g.GameID;

-- 4. Full purchase history, one row per line item
CREATE VIEW PurchaseHistory AS
SELECT
    u.UserID,
    u.Username,
    o.OrderID,
    o.OrderDate,
    g.Title AS GameTitle,
    oi.PurchasePrice
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Order_Items oi ON o.OrderID = oi.OrderID
JOIN Games g ON oi.GameID = g.GameID;

-- 5. Best sellers by copies sold
CREATE VIEW TopSellingGames AS
SELECT
    g.GameID,
    g.Title,
    COUNT(oi.OrderItemID) AS CopiesSold
FROM Games g
JOIN Order_Items oi ON g.GameID = oi.GameID
GROUP BY g.GameID, g.Title
ORDER BY CopiesSold DESC;

-- 6. Revenue attributed to each developer
CREATE VIEW RevenueByDeveloper AS
SELECT
    dev.DeveloperID,
    dev.DeveloperName,
    ROUND(SUM(oi.PurchasePrice), 2) AS TotalRevenue
FROM Developers dev
JOIN Games g ON dev.DeveloperID = g.DeveloperID
JOIN Order_Items oi ON g.GameID = oi.GameID
GROUP BY dev.DeveloperID, dev.DeveloperName;

-- 7. How many users have each game on their wishlist
CREATE VIEW WishlistSummary AS
SELECT
    g.GameID,
    g.Title,
    COUNT(w.UserID) AS WishlistCount
FROM Games g
LEFT JOIN Wishlist w ON g.GameID = w.GameID
GROUP BY g.GameID, g.Title;
```

---

## 4. Functions

```sql
-- 06_Functions.sql

DELIMITER $$

-- 1. Effective price after any active discount
CREATE FUNCTION CalculateDiscountPrice(p_GameID INT)
RETURNS DECIMAL(8,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Price DECIMAL(8,2);
    DECLARE v_Discount DECIMAL(5,2);

    SELECT Price INTO v_Price FROM Games WHERE GameID = p_GameID;

    SELECT DiscountPercent INTO v_Discount
    FROM Discounts
    WHERE GameID = p_GameID
      AND CURDATE() BETWEEN StartDate AND EndDate
    LIMIT 1;

    IF v_Discount IS NULL THEN
        RETURN v_Price;
    ELSE
        RETURN ROUND(v_Price * (1 - v_Discount / 100), 2);
    END IF;
END$$

-- 2. Average rating for a game
CREATE FUNCTION AverageRating(p_GameID INT)
RETURNS DECIMAL(3,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Avg DECIMAL(3,2);
    SELECT ROUND(AVG(Rating), 2) INTO v_Avg FROM Reviews WHERE GameID = p_GameID;
    RETURN IFNULL(v_Avg, 0.00);
END$$

-- 3. Lifetime amount spent by a user (completed orders only)
CREATE FUNCTION TotalSpent(p_UserID INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Total DECIMAL(10,2);
    SELECT IFNULL(SUM(oi.PurchasePrice), 0) INTO v_Total
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    WHERE o.UserID = p_UserID AND o.Status = 'Completed';
    RETURN v_Total;
END$$

-- 4. Number of games a user owns
CREATE FUNCTION GamesOwned(p_UserID INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Count INT;
    SELECT COUNT(*) INTO v_Count FROM Library WHERE UserID = p_UserID;
    RETURN v_Count;
END$$

-- 5. Entire store revenue (completed orders only)
CREATE FUNCTION TotalRevenue()
RETURNS DECIMAL(12,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Revenue DECIMAL(12,2);
    SELECT IFNULL(SUM(oi.PurchasePrice), 0) INTO v_Revenue
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    WHERE o.Status = 'Completed';
    RETURN v_Revenue;
END$$

-- 6. Number of games tagged with a given genre
CREATE FUNCTION GenreGameCount(p_GenreID INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_Count INT;
    SELECT COUNT(*) INTO v_Count FROM Game_Genres WHERE GenreID = p_GenreID;
    RETURN v_Count;
END$$

DELIMITER ;
```

---

## 5. Stored Procedures

```sql
-- 07_Procedures.sql

DELIMITER $$

-- 1. Purchase a game: creates the order, the line item, and (via triggers,
--    see section 6) adds it to the Library and clears it from the Wishlist.
CREATE PROCEDURE PurchaseGame(
    IN p_UserID INT,
    IN p_GameID INT,
    IN p_PaymentMethod VARCHAR(30)
)
BEGIN
    DECLARE v_Price DECIMAL(8,2);
    DECLARE v_OrderID INT;
    DECLARE v_AlreadyOwned INT;

    SELECT COUNT(*) INTO v_AlreadyOwned
    FROM Library WHERE UserID = p_UserID AND GameID = p_GameID;

    IF v_AlreadyOwned > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User already owns this game.';
    END IF;

    SET v_Price = CalculateDiscountPrice(p_GameID);

    START TRANSACTION;
        INSERT INTO Orders (UserID, OrderDate, TotalAmount, PaymentMethod, Status)
        VALUES (p_UserID, NOW(), v_Price, p_PaymentMethod, 'Completed');

        SET v_OrderID = LAST_INSERT_ID();

        INSERT INTO Order_Items (OrderID, GameID, PurchasePrice)
        VALUES (v_OrderID, p_GameID, v_Price);
    COMMIT;
END$$

-- 2. Admin: add a new game, auto-creating the developer/publisher if new
CREATE PROCEDURE AddGame(
    IN p_Title VARCHAR(150),
    IN p_DeveloperName VARCHAR(100),
    IN p_PublisherName VARCHAR(100),
    IN p_Price DECIMAL(8,2),
    IN p_ReleaseDate DATE
)
BEGIN
    DECLARE v_DeveloperID INT DEFAULT NULL;
    DECLARE v_PublisherID INT DEFAULT NULL;

    SELECT DeveloperID INTO v_DeveloperID
    FROM Developers WHERE DeveloperName = p_DeveloperName LIMIT 1;

    IF v_DeveloperID IS NULL THEN
        INSERT INTO Developers (DeveloperName) VALUES (p_DeveloperName);
        SET v_DeveloperID = LAST_INSERT_ID();
    END IF;

    IF p_PublisherName IS NOT NULL THEN
        SELECT PublisherID INTO v_PublisherID
        FROM Publishers WHERE PublisherName = p_PublisherName LIMIT 1;

        IF v_PublisherID IS NULL THEN
            INSERT INTO Publishers (PublisherName) VALUES (p_PublisherName);
            SET v_PublisherID = LAST_INSERT_ID();
        END IF;
    END IF;

    INSERT INTO Games (Title, DeveloperID, PublisherID, Price, ReleaseDate)
    VALUES (p_Title, v_DeveloperID, v_PublisherID, p_Price, p_ReleaseDate);
END$$

-- 3. Apply a discount to a game
CREATE PROCEDURE ApplyDiscount(
    IN p_GameID INT,
    IN p_DiscountPercent DECIMAL(5,2),
    IN p_StartDate DATE,
    IN p_EndDate DATE
)
BEGIN
    INSERT INTO Discounts (GameID, DiscountPercent, StartDate, EndDate)
    VALUES (p_GameID, p_DiscountPercent, p_StartDate, p_EndDate);
END$$

-- 4. Search games by genre name
CREATE PROCEDURE SearchGamesByGenre(IN p_GenreName VARCHAR(50))
BEGIN
    SELECT g.GameID, g.Title, g.Price, g.ReleaseDate
    FROM Games g
    JOIN Game_Genres gg ON g.GameID = gg.GameID
    JOIN Genres gn ON gg.GenreID = gn.GenreID
    WHERE gn.GenreName = p_GenreName;
END$$

-- 5. Full purchase history for one user
CREATE PROCEDURE UserPurchaseHistory(IN p_UserID INT)
BEGIN
    SELECT o.OrderID, g.Title, oi.PurchasePrice, o.OrderDate
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    JOIN Games g ON oi.GameID = g.GameID
    WHERE o.UserID = p_UserID
    ORDER BY o.OrderDate DESC;
END$$

-- 6. Top 10 best-selling games
CREATE PROCEDURE GetTopSellingGames()
BEGIN
    SELECT g.GameID, g.Title, COUNT(oi.OrderItemID) AS CopiesSold
    FROM Games g
    JOIN Order_Items oi ON g.GameID = oi.GameID
    GROUP BY g.GameID, g.Title
    ORDER BY CopiesSold DESC
    LIMIT 10;
END$$

-- 7. Every game a user owns
CREATE PROCEDURE GetUserLibrary(IN p_UserID INT)
BEGIN
    SELECT g.GameID, g.Title, l.PurchaseDate, l.HoursPlayed
    FROM Library l
    JOIN Games g ON l.GameID = g.GameID
    WHERE l.UserID = p_UserID;
END$$

-- 8. Full detail card for one game
CREATE PROCEDURE GetGameDetails(IN p_GameID INT)
BEGIN
    SELECT
        g.GameID,
        g.Title,
        dev.DeveloperName,
        pub.PublisherName,
        GROUP_CONCAT(DISTINCT gn.GenreName SEPARATOR ', ') AS Genres,
        AverageRating(g.GameID) AS AverageRating,
        CalculateDiscountPrice(g.GameID) AS CurrentPrice
    FROM Games g
    LEFT JOIN Developers dev ON g.DeveloperID = dev.DeveloperID
    LEFT JOIN Publishers pub ON g.PublisherID = pub.PublisherID
    LEFT JOIN Game_Genres gg ON g.GameID = gg.GameID
    LEFT JOIN Genres gn ON gg.GenreID = gn.GenreID
    WHERE g.GameID = p_GameID
    GROUP BY g.GameID, g.Title, dev.DeveloperName, pub.PublisherName;
END$$

DELIMITER ;
```

---

## 6. Triggers

```sql
-- 08_Triggers.sql

DELIMITER $$

-- 1. After a game is added to an order, drop it into the buyer's Library
CREATE TRIGGER trg_after_orderitem_insert_library
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;

    INSERT IGNORE INTO Library (UserID, GameID, PurchaseDate, HoursPlayed)
    VALUES (v_UserID, NEW.GameID, CURDATE(), 0);
END$$

-- 2. After purchase, remove the game from the buyer's Wishlist if present
CREATE TRIGGER trg_after_orderitem_remove_wishlist
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;

    DELETE FROM Wishlist WHERE UserID = v_UserID AND GameID = NEW.GameID;
END$$

-- 3. A user can only review a game they own
CREATE TRIGGER trg_before_review_check_library
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    DECLARE v_Owned INT;
    SELECT COUNT(*) INTO v_Owned FROM Library
    WHERE UserID = NEW.UserID AND GameID = NEW.GameID;

    IF v_Owned = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User must own the game before reviewing it.';
    END IF;
END$$

-- 4. Enforce rating range at insert time (belt-and-suspenders alongside the CHECK constraint)
CREATE TRIGGER trg_before_review_check_rating
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    IF NEW.Rating < 1 OR NEW.Rating > 5 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 1 and 5.';
    END IF;
END$$

-- 5. Enforce discount range at insert time
CREATE TRIGGER trg_before_discount_check_range
BEFORE INSERT ON Discounts
FOR EACH ROW
BEGIN
    IF NEW.DiscountPercent < 0 OR NEW.DiscountPercent > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Discount percent must be between 0 and 100.';
    END IF;
END$$

-- 6. Prevent buying a game the user already owns
CREATE TRIGGER trg_before_orderitem_prevent_duplicate
BEFORE INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    DECLARE v_Owned INT;

    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;
    SELECT COUNT(*) INTO v_Owned FROM Library
    WHERE UserID = v_UserID AND GameID = NEW.GameID;

    IF v_Owned > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User already owns this game.';
    END IF;
END$$

-- 7. Block deletion of a game that has already been sold
CREATE TRIGGER trg_before_delete_game_prevent_if_sold
BEFORE DELETE ON Games
FOR EACH ROW
BEGIN
    DECLARE v_SoldCount INT;
    SELECT COUNT(*) INTO v_SoldCount FROM Order_Items WHERE GameID = OLD.GameID;

    IF v_SoldCount > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete a game that has already been sold.';
    END IF;
END$$

DELIMITER ;
```

> **Note on trigger 4 vs. `chk_rating`:** MySQL 8.0.16+ already enforces the `CHECK` constraint on `Reviews.Rating` at the table level. Trigger 4 is kept so the same validation still works if this schema is ever ported to an engine/version without `CHECK` support, and so the error message returned to the app layer is clearer. The same reasoning applies to trigger 5 alongside `chk_discount_percent`.

---

## 7. Sample Data

A small, self-consistent seed set — enough to exercise every view, function, procedure, and trigger. Scale it up to the full target volumes (100 Users / 50 Games / 250 Orders / etc.) by repeating this pattern or writing a loop-based generator once the schema is confirmed working.

```sql
-- 03_Insert_Data.sql

INSERT INTO Developers (DeveloperName, Country, FoundedYear, Website) VALUES
('Rockstar Games', 'USA', 1998, 'https://rockstargames.com'),
('CD Projekt Red', 'Poland', 1994, 'https://cdprojektred.com'),
('FromSoftware', 'Japan', 1986, 'https://fromsoftware.jp'),
('Naughty Dog', 'USA', 1984, 'https://naughtydog.com'),
('Valve', 'USA', 1996, 'https://valvesoftware.com');

INSERT INTO Publishers (PublisherName, Country, Website) VALUES
('Take-Two Interactive', 'USA', 'https://take2games.com'),
('Bandai Namco', 'Japan', 'https://bandainamcoent.com'),
('Sony Interactive Entertainment', 'USA', 'https://sie.com'),
('Electronic Arts', 'USA', 'https://ea.com');

INSERT INTO Genres (GenreName) VALUES
('Action'), ('RPG'), ('Adventure'), ('Strategy'), ('Sports'),
('Simulation'), ('Horror'), ('Shooter'), ('Puzzle'), ('Racing'),
('Platformer'), ('Open World');

INSERT INTO Users (Username, Email, PasswordHash, Country, WalletBalance) VALUES
('arjun_92', 'arjun92@mail.com', 'hash1', 'India', 500.00),
('sara_k', 'sarak@mail.com', 'hash2', 'UK', 120.50),
('mike_j', 'mikej@mail.com', 'hash3', 'USA', 0.00),
('lena_v', 'lenav@mail.com', 'hash4', 'Germany', 75.25),
('tom_h', 'tomh@mail.com', 'hash5', 'Canada', 200.00);

INSERT INTO Games (Title, DeveloperID, PublisherID, Price, ReleaseDate, Description, AgeRating) VALUES
('Red Dead Redemption 2', 1, 1, 2999.00, '2018-10-26', 'Open-world western epic.', 'M'),
('Cyberpunk 2077', 2, NULL, 2499.00, '2020-12-10', 'Dystopian open-world RPG.', 'M'),
('Elden Ring', 3, 2, 3499.00, '2022-02-25', 'Dark fantasy action RPG.', 'M'),
('The Last of Us Part II', 4, 3, 2999.00, '2020-06-19', 'Post-apocalyptic survival action.', 'M'),
('Half-Life: Alyx', 5, NULL, 1999.00, '2020-03-23', 'VR sci-fi shooter.', 'T');

INSERT INTO Game_Genres (GameID, GenreID) VALUES
(1, 1), (1, 12), (2, 2), (2, 12), (3, 2), (3, 1),
(4, 1), (4, 3), (5, 8), (5, 3);

INSERT INTO Discounts (GameID, DiscountPercent, StartDate, EndDate) VALUES
(2, 25.00, '2026-07-20', '2026-08-05'),
(4, 15.00, '2026-07-15', '2026-07-31');

-- Sample purchases (drives Orders -> Order_Items -> Library/Wishlist triggers)
CALL PurchaseGame(1, 1, 'Card');
CALL PurchaseGame(1, 3, 'Wallet');
CALL PurchaseGame(2, 2, 'Card');
CALL PurchaseGame(3, 4, 'PayPal');
CALL PurchaseGame(4, 5, 'Card');

INSERT INTO Wishlist (UserID, GameID) VALUES
(2, 1), (3, 3), (5, 2);

INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES
(1, 1, 5, 'Masterpiece of open-world design.'),
(1, 3, 5, 'Brutal but incredibly rewarding.'),
(2, 2, 3, 'Ambitious but rough around the edges at launch.'),
(3, 4, 4, 'Emotionally intense, great combat.'),
(4, 5, 5, 'Best VR experience available.');
```

---

## 8. Analytical Queries (40)

### Basic (10)

```sql
-- 1. List all users
SELECT * FROM Users;

-- 2. List all games
SELECT * FROM Games;

-- 3. Games priced over ₹1000
SELECT * FROM Games WHERE Price > 1000;

-- 4. All RPG games
SELECT g.*
FROM Games g
JOIN Game_Genres gg ON g.GameID = gg.GameID
JOIN Genres gn ON gg.GenreID = gn.GenreID
WHERE gn.GenreName = 'RPG';

-- 5. Games released after 2022
SELECT * FROM Games WHERE ReleaseDate > '2022-12-31';

-- 6. All developers
SELECT * FROM Developers;

-- 7. All publishers
SELECT * FROM Publishers;

-- 8. All discounts
SELECT * FROM Discounts;

-- 9. Wishlist of a specific user (UserID = 2)
SELECT g.Title, w.AddedDate
FROM Wishlist w
JOIN Games g ON w.GameID = g.GameID
WHERE w.UserID = 2;

-- 10. Library of a specific user (UserID = 1)
SELECT g.Title, l.PurchaseDate, l.HoursPlayed
FROM Library l
JOIN Games g ON l.GameID = g.GameID
WHERE l.UserID = 1;
```

### Intermediate (10)

```sql
-- 1. Games by a specific developer
SELECT g.*
FROM Games g
JOIN Developers d ON g.DeveloperID = d.DeveloperID
WHERE d.DeveloperName = 'Rockstar Games';

-- 2. Games by a specific publisher
SELECT g.*
FROM Games g
JOIN Publishers p ON g.PublisherID = p.PublisherID
WHERE p.PublisherName = 'Electronic Arts';

-- 3. Average price per publisher
SELECT p.PublisherName, ROUND(AVG(g.Price), 2) AS AvgPrice
FROM Games g
JOIN Publishers p ON g.PublisherID = p.PublisherID
GROUP BY p.PublisherName;

-- 4. Number of games per developer
SELECT d.DeveloperName, COUNT(g.GameID) AS GameCount
FROM Developers d
LEFT JOIN Games g ON d.DeveloperID = g.DeveloperID
GROUP BY d.DeveloperName;

-- 5. Number of games per genre
SELECT gn.GenreName, COUNT(gg.GameID) AS GameCount
FROM Genres gn
LEFT JOIN Game_Genres gg ON gn.GenreID = gg.GenreID
GROUP BY gn.GenreName;

-- 6. Users who own more than 10 games
SELECT u.UserID, u.Username, COUNT(l.GameID) AS OwnedGames
FROM Users u
JOIN Library l ON u.UserID = l.UserID
GROUP BY u.UserID, u.Username
HAVING COUNT(l.GameID) > 10;

-- 7. Highest priced game
SELECT * FROM Games ORDER BY Price DESC LIMIT 1;

-- 8. Cheapest game
SELECT * FROM Games ORDER BY Price ASC LIMIT 1;

-- 9. Games without any reviews
SELECT g.*
FROM Games g
LEFT JOIN Reviews r ON g.GameID = r.GameID
WHERE r.ReviewID IS NULL;

-- 10. Games currently discounted
SELECT * FROM CurrentDiscounts;
```

### Advanced JOIN Queries (10)

```sql
-- 1. Full user purchase history
SELECT u.Username, o.OrderID, g.Title, oi.PurchasePrice, o.OrderDate
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
JOIN Order_Items oi ON o.OrderID = oi.OrderID
JOIN Games g ON oi.GameID = g.GameID
ORDER BY o.OrderDate DESC;

-- 2. Total spent by each user
SELECT u.UserID, u.Username, TotalSpent(u.UserID) AS TotalSpent
FROM Users u
ORDER BY TotalSpent DESC;

-- 3. Most purchased game
SELECT g.Title, COUNT(oi.OrderItemID) AS TimesPurchased
FROM Games g
JOIN Order_Items oi ON g.GameID = oi.GameID
GROUP BY g.Title
ORDER BY TimesPurchased DESC
LIMIT 1;

-- 4. Revenue by publisher
SELECT p.PublisherName, ROUND(SUM(oi.PurchasePrice), 2) AS Revenue
FROM Publishers p
JOIN Games g ON p.PublisherID = g.PublisherID
JOIN Order_Items oi ON g.GameID = oi.GameID
GROUP BY p.PublisherName
ORDER BY Revenue DESC;

-- 5. Revenue by developer
SELECT * FROM RevenueByDeveloper ORDER BY TotalRevenue DESC;

-- 6. Average rating by developer
SELECT d.DeveloperName, ROUND(AVG(r.Rating), 2) AS AvgRating
FROM Developers d
JOIN Games g ON d.DeveloperID = g.DeveloperID
JOIN Reviews r ON g.GameID = r.GameID
GROUP BY d.DeveloperName;

-- 7. Average rating by publisher
SELECT p.PublisherName, ROUND(AVG(r.Rating), 2) AS AvgRating
FROM Publishers p
JOIN Games g ON p.PublisherID = g.PublisherID
JOIN Reviews r ON g.GameID = r.GameID
GROUP BY p.PublisherName;

-- 8. Top reviewers
SELECT u.Username, COUNT(r.ReviewID) AS ReviewCount
FROM Users u
JOIN Reviews r ON u.UserID = r.UserID
GROUP BY u.Username
ORDER BY ReviewCount DESC
LIMIT 10;

-- 9. Games tagged with more than one genre
SELECT g.Title, COUNT(gg.GenreID) AS GenreCount
FROM Games g
JOIN Game_Genres gg ON g.GameID = gg.GameID
GROUP BY g.Title
HAVING COUNT(gg.GenreID) > 1;

-- 10. Users who have never placed an order
SELECT u.*
FROM Users u
LEFT JOIN Orders o ON u.UserID = o.UserID
WHERE o.OrderID IS NULL;
```

### Aggregate Queries (5)

```sql
-- 1. Monthly revenue
SELECT DATE_FORMAT(o.OrderDate, '%Y-%m') AS Month,
       ROUND(SUM(oi.PurchasePrice), 2) AS Revenue
FROM Orders o
JOIN Order_Items oi ON o.OrderID = oi.OrderID
GROUP BY Month
ORDER BY Month;

-- 2. Average game price
SELECT ROUND(AVG(Price), 2) AS AveragePrice FROM Games;

-- 3. Total copies sold
SELECT COUNT(*) AS TotalCopiesSold FROM Order_Items;

-- 4. Total games owned across the whole platform
SELECT COUNT(*) AS TotalGamesOwned FROM Library;

-- 5. Store-wide average review score
SELECT ROUND(AVG(Rating), 2) AS AverageReviewScore FROM Reviews;
```

### Nested (Subquery) Queries (5)

```sql
-- 1. Highest rated game
SELECT Title FROM Games
WHERE GameID = (
    SELECT GameID FROM Reviews
    GROUP BY GameID
    ORDER BY AVG(Rating) DESC
    LIMIT 1
);

-- 2. Developer with the highest revenue
SELECT DeveloperName FROM Developers
WHERE DeveloperID = (
    SELECT g.DeveloperID
    FROM Games g
    JOIN Order_Items oi ON g.GameID = oi.GameID
    GROUP BY g.DeveloperID
    ORDER BY SUM(oi.PurchasePrice) DESC
    LIMIT 1
);

-- 3. User who has spent the most
SELECT Username FROM Users
WHERE UserID = (
    SELECT o.UserID
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    GROUP BY o.UserID
    ORDER BY SUM(oi.PurchasePrice) DESC
    LIMIT 1
);

-- 4. Most wishlisted game
SELECT Title FROM Games
WHERE GameID = (
    SELECT GameID FROM Wishlist
    GROUP BY GameID
    ORDER BY COUNT(*) DESC
    LIMIT 1
);

-- 5. Most popular genre by ownership
SELECT GenreName FROM Genres
WHERE GenreID = (
    SELECT gg.GenreID
    FROM Game_Genres gg
    JOIN Library l ON gg.GameID = l.GameID
    GROUP BY gg.GenreID
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
```

---

## 9. How to Run This Project

1. Run **Section 1** to create the database and all 12 tables.
2. Run **Section 4** (Functions) *before* Section 5 (Procedures) and Section 3 (Views), since `CalculateDiscountPrice()` and `AverageRating()` are referenced inside `GetGameDetails` and `CurrentDiscounts`-style logic.
   - Correct load order: **Tables → Indexes → Functions → Procedures → Triggers → Views → Sample Data → Queries.**
3. Run **Section 7** (Sample Data) — this also calls `PurchaseGame()`, which exercises the AFTER-INSERT triggers automatically, so `Library` and `Wishlist` populate correctly without manual inserts.
4. Run any query from **Section 8** to verify.

## 10. Testing Checklist

| Feature | How to verify |
|---|---|
| Library auto-populate trigger | `CALL PurchaseGame(...)`, then check `SELECT * FROM Library` |
| Wishlist auto-clear trigger | Wishlist a game, then buy it, confirm it disappears from `Wishlist` |
| Duplicate ownership block | `CALL PurchaseGame()` twice for the same user/game — second call should raise an error |
| Review-without-ownership block | Try inserting into `Reviews` for a game not in that user's `Library` |
| Rating range | Try inserting `Rating = 6` into `Reviews` |
| Discount range | Try inserting `DiscountPercent = 150` into `Discounts` |
| Game deletion block | Try `DELETE FROM Games WHERE GameID = 1` after a purchase exists |
