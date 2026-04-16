from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = None
    jurisdiction_hint: Optional[str] = None
    regulation_hint: Optional[str] = None
    framework: Optional[str] = "auto"


class Citation(BaseModel):
    source: str
    citation: Optional[str] = None
    page: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    regulations: List[str]
    needs_human_review: bool