import psycopg2

class DatabaseHandler:
    def __init__(self, db_config):
        self.connection = None
        self.cursor = None

        try:
            # Establish the database connection
            self.connection = psycopg2.connect(
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                host=db_config['host'],
                port=db_config['port']
            )
            print("Database connection established.")

            # Create a cursor from the connection
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query, params=None):
        """Execute a query using the cursor."""
        try:
            if self.cursor is None:
                raise Exception("Cursor is not initialized.")

            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_all(self):
        """Fetch all rows from the last executed query."""
        try:
            if self.cursor is None:
                raise Exception("Cursor is not initialized.")

            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def close(self):
        """Close the cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")