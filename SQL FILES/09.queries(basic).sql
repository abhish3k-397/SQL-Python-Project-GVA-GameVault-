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