from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional

from src.database.models import SectionResponse, SectionListResponse
from src.services.section_service import SectionService

# Initialize router
router = APIRouter()

@router.get("/", response_model=SectionListResponse)
async def get_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500)
):
    """Get all sections with pagination."""
    result = await SectionService.get_sections(skip, limit)
    return result

@router.get("/number/{number}", response_model=SectionResponse)
async def get_section_by_number(number: str):
    """Get a section by its number."""
    section = await SectionService.get_section_by_number(number)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with number {number} not found"
        )
    return section

@router.get("/{section_id}", response_model=SectionResponse)
async def get_section_by_id(section_id: str):
    """Get a section by its ID."""
    section = await SectionService.get_section_by_id(section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with ID {section_id} not found"
        )
    return section 