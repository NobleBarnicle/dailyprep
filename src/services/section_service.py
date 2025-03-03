from typing import List, Optional, Dict, Any
import json
import math
from src.database.repository import SectionRepository, PartRepository
from src.database.models import PaginationMetadata

class SectionService:
    """Service for handling Criminal Code section operations."""
    
    @staticmethod
    async def get_sections(skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get all sections with pagination."""
        sections = await SectionRepository.get_all_sections(skip, limit)
        total_items = await SectionRepository.count_sections()
        
        # Calculate pagination metadata
        pagination = PaginationMetadata(
            page=skip // limit + 1,
            page_size=limit,
            total_items=total_items,
            total_pages=math.ceil(total_items / limit)
        )
        
        return {
            "sections": sections,
            "pagination": pagination
        }
    
    @staticmethod
    async def get_section_by_id(section_id: str) -> Optional[Dict[str, Any]]:
        """Get a section by its ID."""
        return await SectionRepository.get_section_by_id(section_id)
    
    @staticmethod
    async def get_section_by_number(number: str) -> Optional[Dict[str, Any]]:
        """Get a section by its number."""
        return await SectionRepository.get_section_by_number(number)
    
    @staticmethod
    async def get_parts() -> List[Dict[str, Any]]:
        """Get all parts of the Criminal Code."""
        return await PartRepository.get_all_parts()
    
    @staticmethod
    async def get_part_by_id(part_id: str) -> Optional[Dict[str, Any]]:
        """Get a part by its ID."""
        return await PartRepository.get_part_by_id(part_id)
    
    @staticmethod
    async def import_data_from_json(file_path: str) -> Dict[str, int]:
        """Import Criminal Code data from a JSON file into the database."""
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        sections_to_insert = []
        parts_to_insert = []
        
        for item in data.get('sections', []):
            if item.get('type') == 'Part':
                parts_to_insert.append(item)
            else:
                sections_to_insert.append(item)
        
        sections_inserted = await SectionRepository.insert_many_sections(sections_to_insert)
        parts_inserted = await PartRepository.insert_many_parts(parts_to_insert)
        
        return {
            'sections_imported': len(sections_inserted),
            'parts_imported': len(parts_inserted)
        }
    
    @staticmethod
    async def build_table_of_contents() -> List[Dict[str, Any]]:
        """Build a hierarchical table of contents for the Criminal Code."""
        parts = await PartRepository.get_all_parts()
        toc = []
        
        for part in parts:
            part_entry = {
                'id': part.get('part_id'),
                'title': part.get('text'),
                'type': 'Part',
                'sections': []
            }
            
            # Find sections that are likely to be in this part
            # This is a simplistic approach and might need refinement
            all_sections = await SectionRepository.get_all_sections(limit=1000)
            
            # Group sections by their parent part (this logic may need to be adjusted based on your data structure)
            current_part = None
            for section in all_sections:
                if section.get('type') == 'Part':
                    current_part = section.get('part_id')
                elif current_part == part.get('part_id'):
                    section_entry = {
                        'id': section.get('section_id'),
                        'number': section.get('number'),
                        'title': section.get('marginal_note') or section.get('text'),
                        'type': section.get('type')
                    }
                    part_entry['sections'].append(section_entry)
            
            toc.append(part_entry)
        
        return toc 