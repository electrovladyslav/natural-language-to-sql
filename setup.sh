#!/bin/bash

# Exit on error
set -e

echo "Setting up Natural Language to SQL Converter..."

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
cd ..

# Initialize the database
echo "Initializing the database..."
cd backend
python3 -c "from database import init_db; init_db()"
cd ..

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js to continue."
    exit 1
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "Setup complete! To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "2. In a new terminal, start the frontend server:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open your browser to http://localhost:3000"
echo "" 