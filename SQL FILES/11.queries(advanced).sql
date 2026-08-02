-- 1. Full user purchase history
SELECT u.Username, o.OrderID, g.Title, oi.PurchasePrice, o.OrderDate
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
JOIN Order_Items oi ON o.OrderID = oi.OrderID
JOIN Games g ON oi.GameID = g.GameID
ORDER BY o.OrderDate DESC;

-- 2. Total spent by each user
SELECT u.UserID, u.Username, TotalSpend(u.UserID) AS TotalSpent
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