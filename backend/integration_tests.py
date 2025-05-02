import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

# Import app modules
from app import app
from llm import SQLGenerator
from database import init_db, execute_query

class LLMIntegrationTestCase(unittest.TestCase):
    """Test case for LLM integration."""
    
    def setUp(self):
        """Set up test client and initialize test database."""
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Initialize test database
        init_db()
    
    @patch('llm.openai.chat.completions.create')
    def test_generate_sql(self, mock_openai_create):
        """Test that LLM generates SQL correctly."""
        # Configure the mock to return a predefined response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.tool_calls = [MagicMock()]
        mock_response.choices[0].message.tool_calls[0].function.arguments = json.dumps({
            "sql_query": "SELECT * FROM customers WHERE age > :min_age"
        })
        mock_openai_create.return_value = mock_response
        
        # Create an instance of SQLGenerator
        generator = SQLGenerator()
        
        # Test the generate_sql method
        sql_template, params = generator.generate_sql("Find customers older than 30")
        
        # Verify the mock was called
        mock_openai_create.assert_called_once()
        
        # Verify the result
        self.assertEqual(sql_template, "SELECT * FROM customers WHERE age > :min_age")
    
    @patch('llm.openai.chat.completions.create')
    def test_extract_params(self, mock_openai_create):
        """Test parameter extraction from natural language query."""
        # Configure the mock to return a predefined response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"min_age": 30}'
        mock_openai_create.return_value = mock_response
        
        # Create an instance of SQLGenerator
        generator = SQLGenerator()
        
        # Test the extract_params method
        params = generator.extract_params("Find customers older than 30")
        
        # Verify the mock was called
        mock_openai_create.assert_called_once()
        
        # Verify the result
        self.assertEqual(params, {"min_age": 30})
    
    @patch('llm.SQLGenerator.process_query')
    def test_api_query_endpoint(self, mock_process_query):
        """Test the /api/query endpoint."""
        # Configure the mock to return a predefined response
        mock_process_query.return_value = (
            "SELECT * FROM customers WHERE age > 30",
            "This query finds all customers who are older than 30 years old.",
            {"min_age": 30}
        )
        
        # Test the API endpoint
        response = self.client.post('/api/query', 
                                   json={"query": "Find customers older than 30"},
                                   content_type='application/json')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["sql_query"], "SELECT * FROM customers WHERE age > 30")
        self.assertEqual(response_data["explanation"], "This query finds all customers who are older than 30 years old.")
        self.assertEqual(response_data["parameters"], {"min_age": 30})
    
    def test_api_health_endpoint(self):
        """Test the /api/health endpoint."""
        # Test the API endpoint
        response = self.client.get('/api/health')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data["status"], "ok")
    
    def test_api_tables_endpoint(self):
        """Test the /api/tables endpoint."""
        # Test the API endpoint
        response = self.client.get('/api/tables')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("customers", response_data)
        self.assertIn("orders", response_data)
    
    def test_api_sample_data_endpoint(self):
        """Test the /api/sample-data endpoint."""
        # Test the API endpoint
        response = self.client.get('/api/sample-data')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("customers", response_data)
        self.assertIn("orders", response_data)
    
    def test_api_example_queries_endpoint(self):
        """Test the /api/example-queries endpoint."""
        # Test the API endpoint
        response = self.client.get('/api/example-queries')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("examples", response_data)
        self.assertTrue(len(response_data["examples"]) > 0)
    
    @patch('llm.openai.chat.completions.create')
    def test_full_query_pipeline(self, mock_openai_create):
        """Test the full pipeline from natural language to SQL execution."""
        # Configure the mock to return a series of predefined responses
        # First call: SQL generation
        sql_response = MagicMock()
        sql_response.choices = [MagicMock()]
        sql_response.choices[0].message.tool_calls = [MagicMock()]
        sql_response.choices[0].message.tool_calls[0].function.arguments = json.dumps({
            "sql_query": "SELECT * FROM customers WHERE age > :min_age",
            "explanation": "Find customers older than the specified age."
        })
        
        # Second call: Parameter extraction
        param_response = MagicMock()
        param_response.choices = [MagicMock()]
        param_response.choices[0].message.content = '{"min_age": 30}'
        
        # Third call: Explanation
        explain_response = MagicMock()
        explain_response.choices = [MagicMock()]
        explain_response.choices[0].message.content = "This query will find all customers who are over 30 years old."
        
        # Configure mock to return different responses on each call
        mock_openai_create.side_effect = [sql_response, param_response, explain_response]
        
        # Test the API endpoint with the full pipeline
        response = self.client.post('/api/query', 
                                   json={"query": "Find customers older than 30"},
                                   content_type='application/json')
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn("results", response_data)
        self.assertIn("sql_query", response_data)
        self.assertIn("explanation", response_data)

if __name__ == '__main__':
    unittest.main()
