import os
from typing import List, Dict

from app.pdf_utils import extract_pages_from_pdf


def load_pdfs_from_folder(folder_path: str) -> List[Dict]:
    all_pages = []

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(folder_path, filename)
        pages = extract_pages_from_pdf(pdf_path)
        all_pages.extend(pages)

    return all_pages
