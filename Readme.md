# Natural Language to SQL Converter

> This project was vibecoded by me and Cursor

This application allows users to convert natural language queries into SQL queries using OpenAI's GPT model.

## Setup Instructions

1. Run the setup script to initialize the environment:
```bash
bash setup.sh
```

This will:
- Create a Python virtual environment
- Install backend dependencies
- Initialize the database
- Install frontend dependencies

2. Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```
Then edit the `.env` file to add your OpenAI API key and other configuration values.

## Running the Application

1. Start the backend server:
```bash
source venv/bin/activate
cd backend
python3 app.py
```

2. In a new terminal, start the frontend server:
```bash
cd frontend
npm run dev
```

3. Open your browser to http://localhost:3000

## Features

- Convert natural language queries to SQL
- View database schema information
- Access sample data
- Get example queries
- Secure SQL query validation
- Query explanation in natural language

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/query` - Process natural language queries
- `GET /api/tables` - Get database schema information
- `GET /api/sample-data` - Get sample data from the database
- `GET /api/example-queries` - Get example natural language queries

## Requirements

- Python 3.x
- Node.js
- OpenAI API key (set as environment variable OPENAI_API_KEY)

## Project Structure

- `backend/`: Python Flask API
  - `app.py`: Main Flask application
  - `llm.py`: LLM integration for natural language to SQL
  - `database.py`: Database connection and query execution
  - `integration_tests.py`: Integration tests
  - `database/`: Database models and schema

- `frontend/`: React web application
  - Built with React, TailwindCSS, and Vite

## Running Tests

To run the integration tests with coverage:

```
cd backend
python3 -m pytest integration_tests.py --cov=. --cov-report=term --cov-report=html
```

## Usage

1. Open your browser to `http://localhost:3000`
2. Enter a natural language query (e.g., "Show me all customers older than 30")
3. View the generated SQL, parameters, and results

## Example Queries

- "Show me all customers who are older than 30"
- "List orders with amounts greater than $500"
- "Find all orders placed in 2023"
- "Which customers have placed more than 2 orders?"
- "What's the total amount spent by customer John Smith?"

## Database Schema

The application uses SQLite with the following tables:

### Customers
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- email (TEXT, UNIQUE)
- age (INTEGER)
- signup_date (TEXT)

### Orders
- id (INTEGER, PRIMARY KEY)
- customer_id (INTEGER, FOREIGN KEY)
- product (TEXT)
- amount (REAL)
- order_date (TEXT)

Relationship: One customer can have many orders (1:N)
