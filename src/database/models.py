from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class Metadata(BaseModel):
    """Metadata for the Criminal Code document."""
    title: str
    creator: str
    issued: str
    modified: str
    subject: str
    language: str

class BaseSectionItem(BaseModel):
    """Base model for sections and related items."""
    type: str
    section_id: Optional[str] = None
    text: str
    
class Part(BaseSectionItem):
    """Model for parts of the Criminal Code."""
    part_id: str
    
class Section(BaseSectionItem):
    """Model for sections of the Criminal Code."""
    number: str
    marginal_note: Optional[str] = None
    
class SubSection(BaseSectionItem):
    """Model for subsections of the Criminal Code."""
    number: str
    
class Paragraph(BaseSectionItem):
    """Model for paragraphs within subsections."""
    letter: Optional[str] = None
    
class CriminalCode(BaseModel):
    """Complete Criminal Code model."""
    metadata: Metadata
    sections: List[Union[Part, Section, SubSection, Paragraph]]

# Pagination metadata models
class PaginationMetadata(BaseModel):
    """Common pagination metadata for list responses."""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    
# API Response Models
class SectionResponse(BaseModel):
    """Response model for a single section."""
    section_id: str
    number: str
    type: str
    text: str
    marginal_note: Optional[str] = None
    
class SectionListResponse(BaseModel):
    """Response model for a list of sections."""
    sections: List[SectionResponse]
    pagination: PaginationMetadata
    
class SearchResult(BaseModel):
    """Model for search results."""
    section_id: str
    number: str
    type: str
    text: str
    score: float
    highlights: Optional[List[str]] = None
    
class SearchResponse(BaseModel):
    """Response model for search queries."""
    results: List[SearchResult]
    pagination: PaginationMetadata 