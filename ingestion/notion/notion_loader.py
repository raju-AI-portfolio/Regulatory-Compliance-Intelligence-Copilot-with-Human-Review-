from notion_client import Client
from app.core.config import settings


def get_notion_client():
    return Client(auth=settings.NOTION_API_KEY)


def fetch_notion_database_pages(database_id: str):
    client = get_notion_client()
    results = []
    has_more = True
    next_cursor = None

    while has_more:
        response = client.databases.query(
            database_id=database_id,
            start_cursor=next_cursor
        ) if next_cursor else client.databases.query(
            database_id=database_id
        )

        results.extend(response.get("results", []))
        has_more = response.get("has_more", False)
        next_cursor = response.get("next_cursor")

    return results
