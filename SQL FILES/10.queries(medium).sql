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