#!/usr/bin/env python3
"""
Script to generate JWT tokens for testing the LLM API endpoints.

IMPORTANT: This script must be run using Poetry to access installed dependencies:
    poetry run python scripts/generate_token.py --username myuser

Or activate the poetry shell first:
    poetry shell
    python scripts/generate_token.py --username myuser
"""

import argparse
import sys
import os
from typing import Optional

# Add parent directory to path to import llm_api modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def generate_token_directly(username: str) -> Optional[str]:
    """
    Generate a JWT token directly using the JWT utilities.
    This bypasses the API and creates a token locally.
    Useful for testing when you don't have API access.
    
    Args:
        username: Username to encode in the token
    
    Returns:
        JWT token string
    """
    try:
        from llm_api.utils.jwt import create_access_token
        
        token_data = {"sub": username}
        token = create_access_token(data=token_data)
        return token
    except ImportError as e:
        print(f"\n❌ Error importing JWT utilities: {e}\n")
        print("This script requires Poetry dependencies to be installed.")
        print("\nTo fix this, run the script with Poetry:")
        print("  poetry run python scripts/generate_token.py --username <username>")
        print("\nOr activate the poetry shell first:")
        print("  poetry shell")
        print("  python scripts/generate_token.py --username <username>")
        print("\nIf dependencies aren't installed, run:")
        print("  poetry install")
        return None
    except Exception as e:
        print(f"Error generating token: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate JWT tokens for testing LLM API endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate token directly (requires Poetry environment)
  poetry run python scripts/generate_token.py --username testuser
  
  # Or if poetry shell is activated:
  python scripts/generate_token.py --username testuser

Note: This script must be run using 'poetry run' to access the required dependencies.
        """
    )
    
    parser.add_argument(
        "--username",
        required=True,
        help="Username for authentication"
    )
    
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Generate token directly
    token = generate_token_directly(args.username)
    
    if token:
        print("\n" + "="*60)
        print("Token generated successfully!")
        print("="*60)
        print(f"\nToken:\n{token}\n")
        print("="*60)
        print("\nUsage example:")
        print(f'curl -X POST "{args.api_url}/chat" \\')
        print('  -H "Authorization: Bearer ' + token + '" \\')
        print('  -H "Content-Type: application/json" \\')
        print('  -d \'{"prompt": "Hello, how are you?"}\'')
        print("\n" + "="*60 + "\n")
    else:
        print("\n❌ Failed to generate token.")
        sys.exit(1)


if __name__ == "__main__":
    main()

