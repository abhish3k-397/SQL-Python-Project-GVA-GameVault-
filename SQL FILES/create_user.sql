-- Create Dedicated Application User for GameVault Python App
CREATE USER IF NOT EXISTS 'gamevault_user'@'localhost' IDENTIFIED BY 'gamevault123';
GRANT ALL PRIVILEGES ON GameVault.* TO 'gamevault_user'@'localhost';
FLUSH PRIVILEGES;
