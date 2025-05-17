import mysql.connector
from mysql.connector import Error
from config.db_config import get_db_config


def check_db_connection():
    try:
        # Get database configuration
        db_config = get_db_config()

        # Establish connection
        connection = mysql.connector.connect(**db_config)

        # Check if connection is successful
        if connection.is_connected():
            print("Successfully connected to the database!")
            # Use server_info property instead of get_server_info()
            db_info = connection.server_info
            print(f"Connected to MySQL Server version: {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"Connected to database: {db_name}")

    except Error as e:
        print(f"Error connecting to the database: {e}")

    finally:
        # Close the connection if it was opened
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")


# Run the check
if __name__ == "__main__":
    check_db_connection()