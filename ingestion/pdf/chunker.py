from typing import List, Dict

from app.chunker import chunk_pages


def build_chunks_from_pages(pages: List[Dict], chunk_size: int = 1000, overlap: int = 150) -> List[Dict]:
    return chunk_pages(pages, chunk_size=chunk_size, overlap=overlap)
