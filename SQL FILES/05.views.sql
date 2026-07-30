-- View 1 for checking what offeres or discounts are available right now

CREATE VIEW CurrentDiscounts AS
SELECT 
	g.GameID,
    g.Title,
    g.Price AS OriginalPrice,
    ROUND(g.Price * (1 - d.DiscountPercent / 100), 2) AS FinalPrice,
    d.StartDate,
    d.EndDate
FROM Games g
JOIN Discounts d
ON g.GameID = d.GameID
WHERE CURDATE() BETWEEN d.StartDate AND d.EndDate;

-- View 2 Rating Summary of games

CREATE VIEW GameRatings AS
SELECT 
	g.GameID,
    g.Title,
    ROUND(AVG(r.Rating),2) AS AverageRating,
    COUNT(r.ReviewID) AS TotalReviews
FROM Games g
LEFT JOIN Reviews r
ON g.GameID = r.GameID 
GROUP BY g.GameID, g.Title;

-- View 3 For viewving the user libraries 

CREATE VIEW UserLibrary AS
SELECT
	u.UserID,
    u.UserName,
    g.GameID,
    g.Title AS GameTitle,
    l.PurchaseDate,
    l.HoursPlayed
FROM Library l
JOIN Users u ON l.UserID = u.UserID
JOIN Games g ON l.GameID = g.GameID;


--  View 4 the purchase history 

CREATE VIEW PurchaseHistory AS
SELECT
	u.UserID,
    u.UserName,
    o.OrderID,
    o.OrderDate,
    g.GameID,
    g.Title AS GameTitle,
    oi.PurchasePrice
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Order_Items oi ON o.OrderID = oi.OrderID
JOIN Games g ON oi.GameID = g.GameID;

-- View 5 See the Best Selling Games

CREATE VIEW TopSellingGames AS
SELECT
	g.GameID,
	g.GameTitle,
	COUNT(oi.OrdeItemID) AS CopiesSold
FROM Games g
JOIN Order_Items oi ON g.GameID = oi.GameID
GROUP BY g.GameID, g.Title
ORDER BY CopiesSold DESC;

-- View 6 Revenue genereated by the developers 

CREATE VIEW RevenueByDeveloper AS
SELECT 
	d.DeveloperID,
    d.DeveloperName,
    ROUND(SUM(oi.PurchasePrice),2) AS TotalRevenue
FROM Developers d
JOIN Games g ON d.DeveloperID = g.DeveloperID
JOIN Order_Items ON g.GameID = oi.GameID
ORDER BY d.DeveloperID , d.DeveloperName;


-- View 7 The Wishlist

CREATE VIEW WishlistSummary AS
SELECT
	g.GameID,
    g.Title,
    COUNT(w.UserID) AS WishlistCount
FROM Games g
JOIN Wishlist w ON g.GameID = w.GameID
GROUP BY g.GameID, g.Title;

