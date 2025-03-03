"""
Script to import Criminal Code data into MongoDB and Elasticsearch.
Run this script after setting up the MongoDB and Elasticsearch instances.
"""
import asyncio
import sys
import os
import json
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.config import connect_to_mongodb, close_mongodb_connection
from src.services.section_service import SectionService
from src.services.search_service import SearchService


async def import_data():
    """Import Criminal Code data into MongoDB and Elasticsearch."""
    print("Starting data import process...")
    
    # Connect to MongoDB
    await connect_to_mongodb()
    
    # Initialize Elasticsearch
    await SearchService.initialize()
    
    # Path to the parsed JSON data
    data_file = Path(__file__).parent.parent.parent / "full_criminal_code.json"
    
    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        return
    
    print(f"Importing data from {data_file}")
    
    try:
        # Import data into MongoDB
        import_results = await SectionService.import_data_from_json(data_file)
        print(f"MongoDB import complete:")
        print(f" - Sections imported: {import_results['sections_imported']}")
        print(f" - Parts imported: {import_results['parts_imported']}")
        
        # Import data into Elasticsearch
        print("Importing data into Elasticsearch...")
        with open(data_file, 'r') as file:
            data = json.load(file)
        
        # Prepare documents for Elasticsearch
        documents = []
        for item in data.get('sections', []):
            if item.get('type') != 'Part':  # Skip parts for now
                # Ensure each document has a section_id
                if 'section_id' not in item:
                    print(f"Warning: Document missing section_id: {item}")
                    # Generate a unique ID if missing
                    if 'number' in item:
                        item['section_id'] = f"generated-{item['number']}"
                    else:
                        # Skip documents without section_id or number
                        print(f"Skipping document without section_id or number: {item}")
                        continue
                documents.append(item)
        
        if documents:
            # Index documents in Elasticsearch
            print(f"Indexing {len(documents)} documents in Elasticsearch...")
            await SearchService.index_bulk_documents(documents)
            print(f"Elasticsearch import complete: {len(documents)} documents indexed")
        else:
            print("No valid documents to index in Elasticsearch")
        
    except Exception as e:
        print(f"Error during import: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close connections
        await close_mongodb_connection()
        await SearchService.close()
        print("Data import process completed.")


if __name__ == "__main__":
    asyncio.run(import_data()) 