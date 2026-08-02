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