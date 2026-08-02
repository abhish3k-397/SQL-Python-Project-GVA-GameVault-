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