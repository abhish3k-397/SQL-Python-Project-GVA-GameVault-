"""
Database Configuration Settings for GameVault CLI Application
"""
import os

# MySQL Database Connection Credentials
# Defaulting to 'gamevault_user' to avoid root unix_socket access restrictions on Linux
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "gamevault_user"),
    "password": os.getenv("DB_PASSWORD", "gamevault123"),
    "database": os.getenv("DB_NAME", "GameVault"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "autocommit": False
}

