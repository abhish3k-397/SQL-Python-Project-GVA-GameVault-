DELIMITER $$

-- Function 1 to Calculate the Discounted Price 
CREATE FUNCTION CalculateDiscountPrice(p_GameID INT) RETURNS DECIMAL(8,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Price DECIMAL(8,2);
    DECLARE v_Discount DECIMAL(5,2);

    SELECT Price INTO v_Price 
    FROM Games 
    WHERE GameID = p_GameID;

    SELECT DiscountPercent INTO v_Discount 
    FROM Discounts 
    WHERE GameID = p_GameID 
    AND CURDATE() BETWEEN StartDate and EndDate
    LIMIT 1;

    IF v_Discount IS NULL THEN
        RETURN v_Price;
    ELSE
        RETURN ROUND(v_Price * (1 - v_Discount / 100), 2);
    END IF;
END $$


-- Function 2 to get the average Rating for a Game

CREATE FUNCTION AverageRating(p_GameID INT) RETURNS DECIMAL(3,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Average DECIMAL(3,2);
    SELECT ROUND(AVG(Rating), 2) INTO v_Average FROM Reviews WHERE GameID = p_GameID;
    RETURN IFNULL(v_Average, 0.00);
END $$

-- Function 3 Lifetime Spend of the user Completed Orders only

CREATE FUNCTION TotalSpend(p_UserID INT) RETURNS DECIMAL(10,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Total DECIMAL(8,2);
    SELECT IFNULL(SUM(oi.PurchasePrice),0.00) INTO v_Total
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    WHERE o.UserID = p_UserID AND o.Status = 'Completed';
    RETURN v_Total;
END $$ 

-- Function 4 Number of User Owned Games 

CREATE FUNCTION GamesOwned(p_UserID INT) RETURNS INT
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Count INT;
    SELECT COUNT(*) INTO v_Count FROM Library WHERE UserID = p_UserID;
    RETURN v_Count;
END $$

-- Function 5 Entire revenue of the store for the completed orders

CREATE FUNCTION TotalRevenue() RETURNS DECIMAL(15,2)
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Revenue DECIMAL(15,2);
    SELECT IFNULL(SUM(oi.PurchasePrice),0.00) INTO v_Revenue
    FROM Orders o
    JOIN Order_Items oi ON o.OrderID = oi.OrderID
    WHERE o.Status = 'Completed';
    RETURN v_Revenue;
END $$

-- Function 6 Total Game count in a particular Genre

CREATE FUNCTION GenreGameCount(p_GenreID INT) RETURNS INT
DETERMINISTIC READS SQL DATA
BEGIN
    DECLARE v_Count INT;
    SELECT COUNT(*) INTO v_Count FROM Game_Genres WHERE GenreID = p_GenreID;
    RETURN v_Count;
END $$

DELIMITER ;
