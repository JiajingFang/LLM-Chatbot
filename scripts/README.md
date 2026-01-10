# Scripts

Utility scripts for testing and development.

## generate_token.py

Generate JWT tokens for testing the LLM API endpoints.

**⚠️ IMPORTANT: This script must be run using Poetry to access the required dependencies.**

### Usage

**Generate token (using Poetry):**
```bash
poetry run python scripts/generate_token.py --username myuser
```

**Or activate Poetry shell first:**
```bash
poetry shell
python scripts/generate_token.py --username myuser
```

**Make sure dependencies are installed:**
```bash
poetry install
```

**Note:** This script generates tokens directly without calling the API. The user must exist in the database for the token to be valid.

### Example Output

The script will output:
1. The generated JWT token
2. A curl command example showing how to use the token

### Testing the Chat Endpoint

After generating a token, you can test the chat endpoint:

```bash
# Get token first (using Poetry)
TOKEN=$(poetry run python scripts/generate_token.py --username myuser | grep -A 1 "Token:" | tail -1)

# Use token in API call
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

Or simply copy the token from the script output and use it in your API calls.

