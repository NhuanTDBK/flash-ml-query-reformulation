from typing import List, Optional
from pydantic import BaseModel


class HighlightElement(BaseModel):
    matchLevel: Optional[str] = ""
    matchedWords: Optional[List[str]] = []
    value: Optional[str] = ""


class HighlightResult(BaseModel):
    author: Optional[HighlightElement]
    story_text: Optional[HighlightElement]
    title: Optional[HighlightElement]


class SearchItemResponse(BaseModel):
    author: Optional[str]
    story_text: Optional[str] = None
    title: str
    created_at: str
    created_at_i: int
    num_comments: int = 0
    objectID: str
    points: int
    story_id: int
    updated_at: str
    _highlightResult: Optional[HighlightResult] = None


class SearchRequest(BaseModel):
    query: str
    page: int = 0
    limit: int = 20
    total_hits: int = 500


class HNSearchResult(BaseModel):
    hits: List[SearchItemResponse]
    page: int
    nbHits: int
    nbPages: int
    hitsPerPage: int
    processingTimeMS: int
    query: str
    params: str
