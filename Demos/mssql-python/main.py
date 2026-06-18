import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SQLServerConnection:
    """
    A class to manage Microsoft SQL Server database connections and operations.
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establish a connection to the SQL Server database.
        """
        try:
            # Build connection string
            connection_string = (
                f"DRIVER={{{os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
                f"SERVER={os.getenv('SQL_SERVER', 'localhost')};"
                f"DATABASE={os.getenv('SQL_DATABASE', 'master')};"
                f"UID={os.getenv('SQL_USERNAME', 'sa')};"
                f"PWD={os.getenv('SQL_PASSWORD', '')};"
                f"TrustServerCertificate={'yes' if os.getenv('SQL_TRUST_CERT', 'false').lower() == 'true' else 'no'}"
            )

            # Establish connection
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("Successfully connected to SQL Server database!")
            return True

        except pyodbc.Error as e:
            print(f"Error connecting to SQL Server: {e}")
            return False

    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return results.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for parameterized queries

        Returns:
            list: Query results as a list of tuples
        """
        try:
            if not self.cursor:
                print("No active database connection. Please connect first.")
                return None

            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # For SELECT queries, fetch and return results
            if query.strip().upper().startswith('SELECT'):
                columns = [column[0] for column in self.cursor.description]
                results = []
                for row in self.cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                # For INSERT, UPDATE, DELETE, commit the transaction
                self.connection.commit()
                print(f"Query executed successfully. Rows affected: {self.cursor.rowcount}")
                return self.cursor.rowcount

        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None

    def close(self):
        """
        Close the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")


def main():
    """
    Main function demonstrating SQL Server connection and operations.
    """
    # Create connection instance
    db = SQLServerConnection()

    # Connect to database
    if db.connect():
        try:
            # Example 1: Get SQL Server version
            print("\n--- SQL Server Version ---")
            version_query = "SELECT @@VERSION as version"
            result = db.execute_query(version_query)
            if result:
                print(result[0]['version'])

            # Example 2: List all databases
            print("\n--- Available Databases ---")
            databases_query = "SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')"
            databases = db.execute_query(databases_query)
            if databases:
                for db_name in databases:
                    print(f"- {db_name['name']}")

            # Example 3: List all tables in current database
            print("\n--- Tables in Current Database ---")
            tables_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            tables = db.execute_query(tables_query)
            if tables:
                for table in tables:
                    print(f"- {table['TABLE_NAME']}")

            # Example 4: Custom query (uncomment to use)
            # print("\n--- Custom Query ---")
            # custom_query = "SELECT * FROM YourTable"
            # custom_results = db.execute_query(custom_query)
            # if custom_results:
            #     for row in custom_results:
            #         print(row)

        except Exception as e:
            print(f"Error during operations: {e}")
        finally:
            # Close connection
            db.close()


if __name__ == "__main__":
    main()
