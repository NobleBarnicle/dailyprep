import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "criminal_code")

# Collections
SECTIONS_COLLECTION = "sections"
PARTS_COLLECTION = "parts"

# MongoDB client instance
client = None
db = None

async def connect_to_mongodb():
    """Connect to MongoDB and initialize database connection."""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        print(f"Connected to MongoDB: {MONGODB_URL}")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongodb_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_database():
    """Get database instance."""
    return db 