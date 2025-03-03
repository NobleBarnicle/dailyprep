from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional

from src.database.models import SearchResponse
from src.services.search_service import SearchService

# Initialize router
router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search_criminal_code(
    q: str = Query(..., description="Search query string"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of results per page")
):
    """Search the Criminal Code with pagination."""
    try:
        search_results = await SearchService.search(q, page, page_size)
        # Convert old format response to new format if needed
        if "total_results" in search_results and "pagination" not in search_results:
            total = search_results.pop("total_results")
            p = search_results.pop("page", page)
            ps = search_results.pop("page_size", page_size)
            search_results["pagination"] = {
                "page": p,
                "page_size": ps,
                "total_items": total,
                "total_pages": (total + ps - 1) // ps
            }
        return search_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        ) 