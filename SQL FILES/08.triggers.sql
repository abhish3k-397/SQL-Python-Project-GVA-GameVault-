-- 08_Triggers.sql

DELIMITER $$

-- 1. After a game is added to an order, drop it into the buyer's Library
CREATE TRIGGER trg_after_orderitem_insert_library
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;

    INSERT IGNORE INTO Library (UserID, GameID, PurchaseDate, HoursPlayed)
    VALUES (v_UserID, NEW.GameID, CURDATE(), 0);
END$$

-- 2. After purchase, remove the game from the buyer's Wishlist if present
CREATE TRIGGER trg_after_orderitem_remove_wishlist
AFTER INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;

    DELETE FROM Wishlist WHERE UserID = v_UserID AND GameID = NEW.GameID;
END$$

-- 3. A user can only review a game they own
CREATE TRIGGER trg_before_review_check_library
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    DECLARE v_Owned INT;
    SELECT COUNT(*) INTO v_Owned FROM Library
    WHERE UserID = NEW.UserID AND GameID = NEW.GameID;

    IF v_Owned = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User must own the game before reviewing it.';
    END IF;
END$$

-- 4. Enforce rating range at insert time (belt-and-suspenders alongside the CHECK constraint)
CREATE TRIGGER trg_before_review_check_rating
BEFORE INSERT ON Reviews
FOR EACH ROW
BEGIN
    IF NEW.Rating < 1 OR NEW.Rating > 5 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rating must be between 1 and 5.';
    END IF;
END$$

-- 5. Enforce discount range at insert time
CREATE TRIGGER trg_before_discount_check_range
BEFORE INSERT ON Discounts
FOR EACH ROW
BEGIN
    IF NEW.DiscountPercent < 0 OR NEW.DiscountPercent > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Discount percent must be between 0 and 100.';
    END IF;
END$$

-- 6. Prevent buying a game the user already owns
CREATE TRIGGER trg_before_orderitem_prevent_duplicate
BEFORE INSERT ON Order_Items
FOR EACH ROW
BEGIN
    DECLARE v_UserID INT;
    DECLARE v_Owned INT;

    SELECT UserID INTO v_UserID FROM Orders WHERE OrderID = NEW.OrderID;
    SELECT COUNT(*) INTO v_Owned FROM Library
    WHERE UserID = v_UserID AND GameID = NEW.GameID;

    IF v_Owned > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User already owns this game.';
    END IF;
END$$

-- 7. Block deletion of a game that has already been sold
CREATE TRIGGER trg_before_delete_game_prevent_if_sold
BEFORE DELETE ON Games
FOR EACH ROW
BEGIN
    DECLARE v_SoldCount INT;
    SELECT COUNT(*) INTO v_SoldCount FROM Order_Items WHERE GameID = OLD.GameID;

    IF v_SoldCount > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete a game that has already been sold.';
    END IF;
END$$

DELIMITER ;