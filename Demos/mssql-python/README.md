# Microsoft SQL Server Python Connector

A Python project for connecting to and interacting with Microsoft SQL Server databases using pyodbc.

## Features

- Secure database connection management
- Environment-based configuration
- Support for parameterized queries
- Error handling and transaction management
- Example queries for common operations

## Prerequisites

- Python 3.7 or higher
- Microsoft SQL Server (local or Azure)
- ODBC Driver for SQL Server installed on your system

### Installing ODBC Driver

**Windows:**
Download and install from [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

**Linux:**
```bash
# Ubuntu/Debian
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

**macOS:**
```bash
brew tap microsoft/mssql-release
brew update
brew install msodbcsql17
```

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env` file and update with your database credentials:
```env
SQL_DRIVER=ODBC Driver 17 for SQL Server
SQL_SERVER=localhost
SQL_DATABASE=your_database_name
SQL_USERNAME=your_username
SQL_PASSWORD=your_password
SQL_TRUST_CERT=false
```

2. For Azure SQL Database, use the server address format: `your-server.database.windows.net`

## Usage

### Basic Usage

Run the main script to test your connection:
```bash
python main.py
```

### Programmatic Usage

```python
from main import SQLServerConnection

# Create connection instance
db = SQLServerConnection()

# Connect to database
if db.connect():
    # Execute a SELECT query
    results = db.execute_query("SELECT * FROM your_table")
    print(results)
    
    # Execute an INSERT query
    db.execute_query(
        "INSERT INTO your_table (column1, column2) VALUES (?, ?)",
        ('value1', 'value2')
    )
    
    # Execute an UPDATE query
    db.execute_query(
        "UPDATE your_table SET column1 = ? WHERE id = ?",
        ('new_value', 1)
    )
    
    # Close connection
    db.close()
```

### Example Queries

```python
# Get SQL Server version
db.execute_query("SELECT @@VERSION as version")

# List all databases
db.execute_query("SELECT name FROM sys.databases")

# List all tables in current database
db.execute_query("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")

# Custom query with parameters
db.execute_query(
    "SELECT * FROM users WHERE age > ? AND department = ?",
    (25, 'Engineering')
)
```

## Project Structure

```
mssql-python/
├── main.py           # Main connection class and example usage
├── requirements.txt  # Python dependencies
├── .env             # Environment configuration (update with your credentials)
└── README.md        # This file
```

## Security Notes

- Never commit the `.env` file to version control
- Use strong passwords for database authentication
- For production, consider using Azure Key Vault or similar secret management
- Enable SSL/TLS encryption for production connections
- Use parameterized queries to prevent SQL injection

## Troubleshooting

### Connection Issues

1. **ODBC Driver not found**: Ensure the ODBC driver is installed and the driver name in `.env` matches your installed version
2. **Authentication failed**: Verify your username and password in `.env`
3. **Server not reachable**: Check firewall settings and ensure SQL Server is configured to accept remote connections

### Common Errors

- **Login timeout**: Increase connection timeout or check network connectivity
- **SSL certificate error**: Set `SQL_TRUST_CERT=true` in `.env` for development (not recommended for production)
- **Database not found**: Verify the database name exists on the server

## License

This project is provided as-is for educational and development purposes.
