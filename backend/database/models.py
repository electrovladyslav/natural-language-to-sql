"""
Database models for the application.
This file is mainly for documentation purposes since we're using SQLite directly.
"""

class Customer:
    """
    Represents a customer in the database.
    
    Attributes:
        id (int): Primary key
        name (str): Customer's full name
        email (str): Customer's email address (unique)
        age (int): Customer's age
        signup_date (str): Date when the customer signed up (YYYY-MM-DD)
    """
    pass

class Order:
    """
    Represents an order in the database.
    
    Attributes:
        id (int): Primary key
        customer_id (int): Foreign key referencing Customer.id
        product (str): Name of the product ordered
        amount (float): Price of the order
        order_date (str): Date when the order was placed (YYYY-MM-DD)
    """
    pass
