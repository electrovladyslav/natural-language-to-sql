import os
import sqlite3
from pathlib import Path

# Database setup
DB_PATH = Path(__file__).parent / "app.db"

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    print(f"Database path: {DB_PATH}")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables and sample data."""
    # Ensure database directory exists
    DB_PATH.parent.mkdir(exist_ok=True)
    
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        signup_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product TEXT NOT NULL,
        amount REAL NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    )
    ''')
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        # Insert sample data for customers
        customers = [
            (1, "John Smith", "john@example.com", 32, "2023-01-15"),
            (2, "Emma Johnson", "emma@example.com", 28, "2023-02-20"),
            (3, "Michael Brown", "michael@example.com", 45, "2023-01-05"),
            (4, "Sophia Williams", "sophia@example.com", 35, "2023-03-10"),
            (5, "Robert Jones", "robert@example.com", 41, "2023-02-01")
        ]
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers)
        
        # Insert sample data for orders
        orders = [
            (1, 1, "Laptop", 1200.00, "2023-02-15"),
            (2, 1, "Mouse", 25.99, "2023-02-15"),
            (3, 2, "Smartphone", 800.00, "2023-03-05"),
            (4, 3, "Headphones", 150.00, "2023-01-20"),
            (5, 3, "Monitor", 300.00, "2023-02-10"),
            (6, 3, "Keyboard", 75.50, "2023-03-15"),
            (7, 4, "Tablet", 450.00, "2023-04-01"),
            (8, 5, "Speaker", 200.00, "2023-02-25"),
            (9, 5, "Printer", 350.00, "2023-03-20"),
            (10, 2, "USB Drive", 35.00, "2023-04-05")
        ]
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
    
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Execute a SQL query and return the results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith(("SELECT", "PRAGMA")):
            # For SELECT queries, return the results
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
            return results
        else:
            # For INSERT, UPDATE, DELETE queries
            conn.commit()
            affected_rows = cursor.rowcount
            conn.close()
            return {"affected_rows": affected_rows}
    
    except Exception as e:
        conn.close()
        raise e

# Call init_db when the module is imported
if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
