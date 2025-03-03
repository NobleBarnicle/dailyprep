"""
Script to test the Criminal Code API endpoints.
Run this after starting the API server.
"""
import asyncio
import aiohttp
import json
from pathlib import Path
import sys

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

API_BASE_URL = "http://localhost:8000/api"

async def test_endpoints():
    """Test the API endpoints."""
    print("Testing Criminal Code API endpoints...")
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        async with session.get("http://localhost:8000/health") as response:
            data = await response.json()
            print(f"Health check: {response.status} - {data}")
        
        # Get first few sections
        async with session.get(f"{API_BASE_URL}/sections?limit=5") as response:
            data = await response.json()
            print(f"\nSections: {response.status}")
            for section in data.get("sections", [])[:3]:  # Print only first 3 for brevity
                print(f" - Section {section.get('number')}: {section.get('marginal_note', '')[:50]}...")
        
        # Get table of contents
        async with session.get(f"{API_BASE_URL}/table-of-contents") as response:
            data = await response.json()
            print(f"\nTable of Contents: {response.status}")
            for part in data[:3]:  # Print only first 3 parts for brevity
                print(f" - Part: {part.get('title')[:50]}...")
                if part.get('sections'):
                    print(f"   - First section: {part['sections'][0].get('number')} - {part['sections'][0].get('title', '')[:30]}...")
        
        # Try a search query
        search_query = "robbery"
        async with session.get(f"{API_BASE_URL}/search?q={search_query}&page=1&page_size=3") as response:
            data = await response.json()
            print(f"\nSearch for '{search_query}': {response.status}")
            if response.status == 200:
                print(f" - Total results: {data.get('total_results', 0)}")
                for result in data.get("results", []):
                    print(f" - Result: Section {result.get('number')} - Score: {result.get('score')}")
                    if result.get("highlights"):
                        print(f"   Highlight: {result['highlights'][0][:100]}...")
            else:
                print(f" - Error: {data}")

if __name__ == "__main__":
    asyncio.run(test_endpoints()) 