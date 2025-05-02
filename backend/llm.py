import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import openai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_queries.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Set up the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class SQLGenerator:
    """
    Class to handle the conversion of natural language to SQL using OpenAI's LLM.
    """
    
    def __init__(self):
        """Initialize the SQL Generator with database schema information."""
        self.schema_info = """
        Table: customers
        Columns:
        - id (INTEGER, PRIMARY KEY)
        - name (TEXT, NOT NULL)
        - email (TEXT, UNIQUE, NOT NULL)
        - age (INTEGER)
        - signup_date (TEXT, format: YYYY-MM-DD)

        Table: orders
        Columns:
        - id (INTEGER, PRIMARY KEY)
        - customer_id (INTEGER, FOREIGN KEY referencing customers.id)
        - product (TEXT, NOT NULL)
        - amount (REAL, NOT NULL)
        - order_date (TEXT, NOT NULL, format: YYYY-MM-DD)

        Relationship: One customer can have many orders (1:N relationship)
        """
        logging.info("SQLGenerator initialized with schema info")
        
    def extract_params(self, nl_query: str) -> Dict[str, Any]:
        """
        Extract parameters from natural language query to be used in SQL.
        
        Args:
            nl_query: Natural language query string
            
        Returns:
            Dictionary of parameter names and values
        """
        logging.info(f"Extracting parameters from query: {nl_query}")
        prompt = f"""
        Based on the following natural language query, extract all values that would be used as parameters in a SQL query.
        
        Natural language query: {nl_query}
        
        Return ONLY a JSON object where each key is a parameter name and each value is the extracted value.
        Don't include any other explanations, text, or formatting. Only the valid JSON object.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts parameters from natural language queries for SQL."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            
            result = response.choices[0].message.content.strip()
            
            # Attempt to parse as JSON (might be wrapped in ```json or other formatting)
            try:
                params = json.loads(result)
                logging.info(f"Extracted parameters: {params}")
                return params
            except json.JSONDecodeError:
                # Try to extract JSON if it's wrapped in markdown code blocks
                if "```json" in result and "```" in result.split("```json", 1)[1]:
                    json_str = result.split("```json", 1)[1].split("```", 1)[0].strip()
                    params = json.loads(json_str)
                    logging.info(f"Extracted parameters: {params}")
                    return params
                elif "```" in result and "```" in result.split("```", 1)[1]:
                    json_str = result.split("```", 1)[1].split("```", 1)[0].strip()
                    params = json.loads(json_str)
                    logging.info(f"Extracted parameters: {params}")
                    return params
                else:
                    logging.warning("Failed to extract parameters, returning empty dict")
                    return {}
        
        except Exception as e:
            logging.error(f"Error extracting parameters: {e}")
            return {}
    
    def generate_sql(self, nl_query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Generate SQL query from natural language using OpenAI's function calling.
        
        Args:
            nl_query: Natural language query string
            
        Returns:
            Tuple of (SQL query template, parameters dictionary)
        """
        logging.info(f"Generating SQL for query: {nl_query}")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_sql_query",
                    "description": "Generate a parameterized SQL query based on a natural language request",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "The parameterized SQL query with placeholders like :param_name"
                            },
                            "explanation": {
                                "type": "string",
                                "description": "A brief explanation of what the SQL query does"
                            }
                        },
                        "required": ["sql_query"]
                    }
                }
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a SQL expert that generates parameterized SQLite queries. Use the following database schema information: {self.schema_info}"},
                    {"role": "user", "content": f"Generate a parameterized SQL query for this request: {nl_query}"}
                ],
                tools=tools,
                tool_choice={"type": "function", "function": {"name": "generate_sql_query"}}
            )
            
            tool_call = response.choices[0].message.tool_calls[0]
            function_args = json.loads(tool_call.function.arguments)
            
            sql_template = function_args.get("sql_query", "")
            explanation = function_args.get("explanation", "")
            
            logging.info(f"Generated SQL template: {sql_template}")
            logging.info(f"Query explanation: {explanation}")
            
            # Extract parameters
            params = self.extract_params(nl_query)
            
            return sql_template, params
            
        except Exception as e:
            logging.error(f"Error generating SQL: {e}")
            return "", {}
    
    def validate_sql(self, sql_query: str) -> bool:
        """
        Validate the generated SQL query for security and correctness.
        
        Args:
            sql_query: SQL query to validate
            
        Returns:
            Boolean indicating if the query is valid
        """
        logging.info(f"Validating SQL query: {sql_query}")
        # List of disallowed SQL operations for security
        dangerous_operations = [
            "DROP", "TRUNCATE", "ALTER", 
            "CREATE USER", "GRANT", "REVOKE",
            "EXEC", "EXECUTE"
        ]
        
        # Check for dangerous operations
        upper_query = sql_query.upper()
        for operation in dangerous_operations:
            if operation in upper_query:
                logging.warning(f"Query contains dangerous operation: {operation}")
                return False
        
        # Ensure the query only accesses allowed tables
        allowed_tables = ["customers", "orders"]
        is_using_allowed_tables = False
        
        for table in allowed_tables:
            if table in sql_query.lower():
                is_using_allowed_tables = True
                break
        
        if not is_using_allowed_tables:
            logging.warning("Query doesn't use any allowed tables")
            return False
        
        logging.info("SQL query validation passed")
        return True
    
    def apply_params(self, sql_template: str, params: Dict[str, Any]) -> str:
        """
        Apply parameters to a SQL template.
        
        Args:
            sql_template: SQL query template with parameter placeholders
            params: Dictionary of parameter names and values
            
        Returns:
            SQL query with parameters applied
        """
        logging.info(f"Applying parameters to SQL template: {sql_template}")
        logging.info(f"Parameters: {params}")
        # Simple parameter substitution 
        # In a production app, this should use proper parameterized queries
        query = sql_template
        for param_name, param_value in params.items():
            placeholder = f":{param_name}"
            if placeholder in query:
                # For string values, add quotes
                if isinstance(param_value, str):
                    # Prevent SQL injection by escaping single quotes
                    safe_value = param_value.replace("'", "''")
                    query = query.replace(placeholder, f"'{safe_value}'")
                else:
                    query = query.replace(placeholder, str(param_value))
        
        logging.info(f"Final SQL query: {query}")
        return query
    
    def process_query(self, nl_query: str) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
        """
        Process a natural language query into a SQL query.
        
        Args:
            nl_query: Natural language query
            
        Returns:
            Tuple of (SQL query, explanation, parameters dictionary)
            If query generation failed, SQL query will be None
        """
        logging.info(f"Processing natural language query: {nl_query}")
        sql_template, params = self.generate_sql(nl_query)
        
        if not sql_template:
            logging.error("Failed to generate SQL template")
            return None, "Failed to generate SQL query", {}
        
        # Apply parameters to the template
        sql_query = self.apply_params(sql_template, params)
        
        # Validate the SQL
        if not self.validate_sql(sql_query):
            logging.error("SQL validation failed")
            return None, "Generated SQL query does not pass security validation", {}
        
        try:
            # Generate an explanation of the query
            prompt = f"""
            Explain the following SQL query in simple terms:
            {sql_query}
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that explains SQL queries in simple language."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            explanation = response.choices[0].message.content.strip()
            logging.info(f"Generated explanation: {explanation}")
            
            return sql_query, explanation, params
            
        except Exception as e:
            logging.error(f"Error explaining SQL: {e}")
            return sql_query, "SQL query processed successfully", params
