import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

# Import database functions from the package
from database import init_db, execute_query
from llm import SQLGenerator

# Initialize the app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the SQL generator
sql_generator = SQLGenerator()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for the API."""
    return jsonify({"status": "ok", "message": "API is running"}), 200

@app.route('/api/query', methods=['POST'])
def process_query():
    """
    Process a natural language query and convert it to SQL.
    
    Expected JSON payload:
    {
        "query": "natural language query string"
    }
    """
    try:
        # Get the request data
        data = request.json
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in request"
            }), 400
        
        nl_query = data['query']
        
        # Process the query with the LLM
        sql_query, explanation, params = sql_generator.process_query(nl_query)
        
        if not sql_query:
            return jsonify({
                "error": explanation
            }), 400
        
        # Execute the SQL query
        try:
            results = execute_query(sql_query)
            
            return jsonify({
                "natural_language_query": nl_query,
                "sql_query": sql_query,
                "parameters": params,
                "explanation": explanation,
                "results": results
            }), 200
            
        except Exception as e:
            error_msg = str(e)
            stack_trace = traceback.format_exc()
            
            return jsonify({
                "error": f"Error executing SQL query: {error_msg}",
                "sql_query": sql_query,
                "stack_trace": stack_trace
            }), 500
    
    except Exception as e:
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        
        return jsonify({
            "error": f"Error processing query: {error_msg}",
            "stack_trace": stack_trace
        }), 500

@app.route('/api/tables', methods=['GET'])
def get_tables():
    """Get the database schema information."""
    try:
        customers_schema = execute_query("PRAGMA table_info(customers)")
        orders_schema = execute_query("PRAGMA table_info(orders)")
        
        return jsonify({
            "customers": customers_schema,
            "orders": orders_schema
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error fetching schema: {str(e)}"
        }), 500

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample data from the database."""
    try:
        # Limit to first 10 rows for each table
        customers = execute_query("SELECT * FROM customers LIMIT 10")
        orders = execute_query("SELECT * FROM orders LIMIT 10")
        
        return jsonify({
            "customers": customers,
            "orders": orders
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Error fetching sample data: {str(e)}"
        }), 500

@app.route('/api/example-queries', methods=['GET'])
def get_example_queries():
    """Get example natural language queries."""
    examples = [
        "Show me all customers who are older than 30",
        "List orders with amounts greater than $500",
        "Find all orders placed in 2023",
        "Which customers have placed more than 2 orders?",
        "What's the total amount spent by customer John Smith?",
        "Show me all customers and their order counts"
    ]
    
    return jsonify({
        "examples": examples
    }), 200

if __name__ == '__main__':
    # Run the app in debug mode
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
