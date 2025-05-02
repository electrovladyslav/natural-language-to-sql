#!/usr/bin/env python3
import os
import subprocess
import sys

def run_tests_with_coverage():
    """Run tests with coverage."""
    print("Running tests with coverage...")
    
    # Run tests with pytest-cov
    result = subprocess.run([
        "pytest", 
        "integration_tests.py", 
        "--cov=.", 
        "--cov-report=term", 
        "--cov-report=html"
    ], capture_output=True, text=True)
    
    # Print output
    print(result.stdout)
    if result.stderr:
        print("Errors:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    # Return exit code
    return result.returncode

if __name__ == "__main__":
    # Run tests
    exit_code = run_tests_with_coverage()
    
    # Exit with the same code
    sys.exit(exit_code) 