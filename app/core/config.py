import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    COHERE_RERANK_MODEL = os.getenv("COHERE_RERANK_MODEL", "rerank-english-v3.0")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "compliance-rag")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
    NOTION_GDPR_DB_ID = os.getenv("NOTION_GDPR_DB_ID", "")
    AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
    AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "")
    AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    APP_ENV = os.getenv("APP_ENV", "dev")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    N8N_PENDING_REVIEW_WEBHOOK_URL = os.getenv("N8N_PENDING_REVIEW_WEBHOOK_URL", "")

settings = Settings()
