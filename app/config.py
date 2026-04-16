import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
PDF_FOLDER = os.getenv("PDF_FOLDER", "data/pdfs")
INDEX_FOLDER = os.getenv("INDEX_FOLDER", "indexes")