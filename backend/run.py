#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Make sure we can import the local modules
sys.path.insert(0, str(Path(__file__).parent))

# Import the app and database module
import database
from app import app

if __name__ == "__main__":
    # Initialize the database
    print("Initializing database...")
    database.init_db()
    
    # Run the app
    print("Starting Flask application...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 