from typing import List, Optional, Dict, Any
from bson import ObjectId

from src.database.config import get_database, SECTIONS_COLLECTION, PARTS_COLLECTION

class SectionRepository:
    """Repository for interacting with sections in the database."""
    
    @staticmethod
    async def get_all_sections(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all sections with pagination."""
        db = get_database()
        cursor = db[SECTIONS_COLLECTION].find().skip(skip).limit(limit)
        sections = await cursor.to_list(length=limit)
        return sections
    
    @staticmethod
    async def count_sections() -> int:
        """Count total number of sections in the database."""
        db = get_database()
        count = await db[SECTIONS_COLLECTION].count_documents({})
        return count
    
    @staticmethod
    async def get_section_by_id(section_id: str) -> Optional[Dict[str, Any]]:
        """Get a section by its ID."""
        db = get_database()
        section = await db[SECTIONS_COLLECTION].find_one({"section_id": section_id})
        return section
    
    @staticmethod
    async def get_section_by_number(number: str) -> Optional[Dict[str, Any]]:
        """Get a section by its number."""
        db = get_database()
        section = await db[SECTIONS_COLLECTION].find_one({"number": number})
        return section
    
    @staticmethod
    async def insert_section(section_data: Dict[str, Any]) -> str:
        """Insert a new section into the database."""
        db = get_database()
        result = await db[SECTIONS_COLLECTION].insert_one(section_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def insert_many_sections(sections_data: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple sections into the database."""
        db = get_database()
        result = await db[SECTIONS_COLLECTION].insert_many(sections_data)
        return [str(id) for id in result.inserted_ids]
    
    @staticmethod
    async def update_section(section_id: str, section_data: Dict[str, Any]) -> bool:
        """Update a section by its ID."""
        db = get_database()
        result = await db[SECTIONS_COLLECTION].update_one(
            {"section_id": section_id}, {"$set": section_data}
        )
        return result.modified_count > 0

class PartRepository:
    """Repository for interacting with parts in the database."""
    
    @staticmethod
    async def get_all_parts() -> List[Dict[str, Any]]:
        """Get all parts of the Criminal Code."""
        db = get_database()
        cursor = db[PARTS_COLLECTION].find()
        parts = await cursor.to_list(length=100)  # Assuming not many parts
        return parts
    
    @staticmethod
    async def get_part_by_id(part_id: str) -> Optional[Dict[str, Any]]:
        """Get a part by its ID."""
        db = get_database()
        part = await db[PARTS_COLLECTION].find_one({"part_id": part_id})
        return part
    
    @staticmethod
    async def insert_part(part_data: Dict[str, Any]) -> str:
        """Insert a new part into the database."""
        db = get_database()
        result = await db[PARTS_COLLECTION].insert_one(part_data)
        return str(result.inserted_id)
    
    @staticmethod
    async def insert_many_parts(parts_data: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple parts into the database."""
        db = get_database()
        result = await db[PARTS_COLLECTION].insert_many(parts_data)
        return [str(id) for id in result.inserted_ids] 