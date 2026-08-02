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
CALL PurchaseGame(1, 1, 'Credit Card');
CALL PurchaseGame(1, 3, 'Wallet');
CALL PurchaseGame(2, 2, 'Credit Card');
CALL PurchaseGame(3, 4, 'PayPal');
CALL PurchaseGame(4, 5, 'Credit Card');

INSERT INTO Wishlist (UserID, GameID) VALUES
(2, 1), (3, 3), (5, 2);

INSERT INTO Reviews (UserID, GameID, Rating, Comment) VALUES
(1, 1, 5, 'Masterpiece of open-world design.'),
(1, 3, 5, 'Brutal but incredibly rewarding.'),
(2, 2, 3, 'Ambitious but rough around the edges at launch.'),
(3, 4, 4, 'Emotionally intense, great combat.'),
(4, 5, 5, 'Best VR experience available.');