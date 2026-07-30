USE GameVault;
-- TOTAL 12 TABLES 
-- TABLE 1
CREATE TABLE Users(
	UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
	PasswordHash VARCHAR(255) NOT NULL,
    Country VARCHAR(50),
    JoinDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    WalletBalance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT chk_wallet_balance CHECK (WalletBalance >= 0)
);
-- TABLE 2
CREATE TABLE Developers(
	DeveloperID INT PRIMARY KEY AUTO_INCREMENT,
    DeveloperName VARCHAR(100) NOT NULL,
    Country VARCHAR(50),
    FoundedYear SMALLINT,
    Website VARCHAR(150),
    CONSTRAINT chk_founded_year CHECK (FoundedYear <= YEAR(CURRENT_DATE()))
);
-- TABLE 3
CREATE TABLE Publishers(
	PublisherID INT PRIMARY KEY AUTO_INCREMENT,
    PublisherName VARCHAR(100) NOT NULL,
    Country VARCHAR(50),
    Website VARCHAR(150)
);

-- TABLE 4

CREATE TABLE Games(
	GameID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(150) NOT NULL,
    DeveloperID INT NOT NULL,
    PublisherID INT,
    Price DECIMAL(10,2) NOT NULL,
    ReleaseDate DATE,
    Description TEXT,
    AgeRating VARCHAR(10),
    CONSTRAINT chk_age_rating CHECK (AgeRating IN ('E','E10+','T','M','AO','RP','PEGI 3','PEGI 7','PEGI 12','PEGI 16','PEGI 18')),
    CONSTRAINT chk_price CHECK (Price >= 0),
    CONSTRAINT fk_game_developer FOREIGN KEY(DeveloperID) REFERENCES Developers(DeveloperID) ON DELETE RESTRICT,
    CONSTRAINT fk_game_publisher FOREIGN KEY(PublisherID) REFERENCES Publishers(PublisherID) ON DELETE SET NULL
);

-- TABLE 5

CREATE TABLE Genres(
	GenreID INT PRIMARY KEY AUTO_INCREMENT,
    GenreName VARCHAR(50) NOT NULL UNIQUE
);
-- TABLE 6
CREATE TABLE Game_Genres(
	GameID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (GameID,GenreID),
    CONSTRAINT fk_gg_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE,
    CONSTRAINT fk_gg_genre FOREIGN KEY(GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE
    
);

-- TABLE 7

CREATE TABLE Orders(
	OrderID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    OrderDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PaymentMethod VARCHAR(30) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    CHECK (PaymentMethod IN ('Wallet','Credit Card','Debit Card','UPI','PayPal')),
    CONSTRAINT chk_total_amount CHECK (TotalAmount >= 0),
    CONSTRAINT chk_order_status CHECK (Status IN('Pending','Completed','Cancelled','Refunded')),
    CONSTRAINT fk_order_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- TABLE 8
CREATE TABLE Order_Items(
	OrderItemID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT NOT NULL,
    GameID INT NOT NULL,
    PurchasePrice DECIMAL(10,2) NOT NULL,
    CONSTRAINT chk_purchase_price CHECK (PurchasePrice >= 0),
    CONSTRAINT uq_order_game UNIQUE(OrderID, GameID),
    CONSTRAINT fk_oi_order FOREIGN KEY(OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_oi_games FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE RESTRICT
);

-- TABLE 9

CREATE TABLE Library(
	UserID INT NOT NULL,
    GameID INT NOT NULL,
    PurchaseDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    HoursPlayed DECIMAL(6,1) NOT NULL DEFAULT 0,
    PRIMARY KEY(UserID, GameID),
    CONSTRAINT chk_hours_played CHECK (HoursPlayed >= 0),
    CONSTRAINT fk_lib_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_lib_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

-- TABLE 10
CREATE TABLE Wishlist(
	UserID INT NOT NULL,
    GameID INT NOT NULL,
    AddedDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    PRIMARY KEY(UserID, GameID),
    CONSTRAINT fk_wl_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_wl_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);

-- TABLE 11

CREATE TABLE Reviews(
	ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    GameID INT NOT NULL,
    Rating TINYINT NOT NULL,
    Comment TEXT,
    ReviewDate DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT uq_user_game_review UNIQUE(UserID, GameID),
    CONSTRAINT chk_rating CHECK (RATING BETWEEN 1 AND 5),
    CONSTRAINT fk_rev_user FOREIGN KEY(UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    CONSTRAINT fk_rev_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);


-- TABLE 12

CREATE TABLE Discounts(
	DiscountID INT PRIMARY KEY AUTO_INCREMENT,
    GameID INT NOT NULL,
    DiscountPercent DECIMAL(5,2) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    CONSTRAINT chk_discount_percent CHECK (DiscountPercent BETWEEN 0 AND 100),
    CONSTRAINT chk_discount_dates CHECK (EndDate >= StartDate),
    CONSTRAINT fk_disc_game FOREIGN KEY(GameID) REFERENCES Games(GameID) ON DELETE CASCADE
);