-- Procedure 1 Buying a Game
DELIMITTER $$

CREATE PROCEDURE PurchaseGame(
    IN p_UserID INT,
    IN p_GameID INT,
    IN p_PaymentMethod VARCHAR(255)
)
BEGIN
    DECLARE v_Price DECIMAL(10,2);
    DECLARE v_OrderID INT;
    DECLARE v_AlreadyOwned INT;
    
    SELECT COUNT(*) INTO v_AlreadyOwned
    FROM Library WHERE UserID = p_UserID AND GameID = p_GameID;

    IF v_AlreadyOwned > 0 THEN 
        SET SQLSTATE '45000' SET MESSAGE_TEXT 'You already own the Game';
    END IF;

    SET v_Price = CalculateDiscountPrice(p_GameID);

    START TRANSACTION;
        INSERT INTO Orders (UserID,OrderDate, TotalAmount,PaymentMethod,Status)
        VALUES (p_UserID,NOW(),v_Price,p_PaymentMethod,'Completed');

        SET v_OrderID = LAST_INSERT_ID();

        INSERT INTO Order_Items(OrderID,GameID,PurchasePrice)
        VALUES (v_OrderID,p_GameID,v_Price);
    COMMIT;
END$$


-- Add Game; Admin adds a new Game and auto creates the dev or publisher if not known 

CREATE PROCEDURE AddGame(
    IN p_Title VARCHAR(150),
    IN p_DeveloperName VARCHAR(100),
    IN p_PublisherName VARCHAR(100),
    IN p_Price DECIMAL(10,2),
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
        SELECT PublisherID into v_PublisherID
        FROM Publishers WHERE PublsherName = p_PublisherName LIMIT 1;

        IF v_PublisherID IS NULL THEN
            INSERT INTO Publisehrs (PublisherName) VALUES (p_PublisherName);
            SET v_PublisherID = LAST_INSERT_ID();
        END IF;
    END IF;

    INSERT INTO Games (Title, DeveloperID, PublisherID, Price, ReleaseDate)
    VALUES (p_Title,v_DeveloperID,v_PublisherID,p_Price,p_ReleaseDate);
END$$

-- Procedure 3: Applying Discount to Games

CREATE PROCEDURE  ApplyDiscount(
    IN p_GameID INT,
    IN p_DiscountPercent DECIMAL(5,2),
    IN p_StartDate DATE,
    IN p_EndDate DATE
)

BEGIN
    INSERT INTO Discounts (GameID, DiscountPercent, StartDate, EndDate)
    VALUES (p_GameID, p_DiscountPercent, p_StartDate, p_EndDate);
END$$

-- Procedure 4: Search Games by Genere Name 

CREATE PROCEDURE SearchGamebyGenere