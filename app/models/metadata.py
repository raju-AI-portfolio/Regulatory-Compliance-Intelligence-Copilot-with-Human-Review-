from pydantic import BaseModel
from typing import Optional


class ChunkMetadata(BaseModel):
    source_document: str
    regulation: str
    jurisdiction: str
    section_type: Optional[str] = None
    section_number: Optional[str] = None
    section_title: Optional[str] = None
    article_number: Optional[str] = None
    article_title: Optional[str] = None
    page_number: Optional[int] = None
    effective_date: Optional[str] = None
    version: Optional[str] = None
    citation: Optional[str] = None
    source_type: Optional[str] = None   # pdf / notion
    namespace: Optional[str] = None     # gdpr_pdf / gdpr_notion / hipaa_pdf / nist_pdf
    is_deprecated: bool = False
