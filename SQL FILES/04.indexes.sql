CREATE INDEX idx_game_title      ON Games(Title);
CREATE INDEX idx_game_price      ON Games(Price);
CREATE INDEX idx_game_developer  ON Games(DeveloperID);
CREATE INDEX idx_order_date      ON Orders(OrderDate);
CREATE INDEX idx_review_rating   ON Reviews(Rating);
CREATE INDEX idx_discount_dates  ON Discounts(StartDate, EndDate);