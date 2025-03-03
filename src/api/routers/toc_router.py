from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any

from src.services.section_service import SectionService

router = APIRouter()

@router.get("/")
async def get_table_of_contents() -> List[Dict[str, Any]]:
    """
    Get a hierarchical table of contents for the Criminal Code.
    This endpoint provides the structure of the Criminal Code,
    organizing sections by parts for easier navigation.
    """
    try:
        toc = await SectionService.build_table_of_contents()
        return toc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error building table of contents: {str(e)}"
        ) 