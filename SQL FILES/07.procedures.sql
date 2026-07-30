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
        