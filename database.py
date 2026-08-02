"""
Database Connection Manager using Python Context Manager Pattern
Handles auto-connection, dictionary cursor creation, transactions (commit/rollback), and error handling.
"""

from config import DB_CONFIG

class DatabaseConnection:
    """
    Context Manager for MySQL Database Operations.
    Usage:
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM Games")
            results = cursor.fetchall()
    """
    def __init__(self, config=None):
        self.config = config or DB_CONFIG
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            import mysql.connector
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.cursor
        except ImportError:
            try:
                import pymysql
                import pymysql.cursors
                cfg = self.config.copy()
                if "autocommit" in cfg:
                    del cfg["autocommit"]
                cfg["cursorclass"] = pymysql.cursors.DictCursor
                self.connection = pymysql.connect(**cfg)
                self.cursor = self.connection.cursor()
                return self.cursor
            except ImportError:
                raise RuntimeError(
                    "❌ Neither 'mysql-connector-python' nor 'pymysql' is installed. "
                    "Please run: pip install mysql-connector-python"
                )
        except Exception as err:
            print(f"\n❌ Failed to connect to MySQL database '{self.config['database']}': {err}")
            raise err

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type:
                # Rollback transaction on error
                self.connection.rollback()
            else:
                # Commit transaction on success
                self.connection.commit()
            if self.cursor:
                self.cursor.close()
            self.connection.close()
