#!/usr/bin/env python3
"""
Run the Criminal Code API.
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
host = os.getenv("API_HOST", "0.0.0.0")
port = int(os.getenv("API_PORT", "8000"))
debug = os.getenv("DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    print(f"Starting Criminal Code API on http://{host}:{port}")
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=debug
    ) 