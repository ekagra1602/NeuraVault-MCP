from datetime import datetime
from typing import Dict, List
from typing import Optional

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """A single piece of memory stored for an LLM / user."""

    user_id: str
    llm: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemoryStore:
    """Simple in-process memory store.

    This is suitable for prototyping; swap with a database or external cache in production.
    """

    def __init__(self) -> None:
        self._store: Dict[str, List[MemoryItem]] = {}

    def add(self, item: MemoryItem) -> None:
        """Add a memory item to the store."""
        self._store.setdefault(item.user_id, []).append(item)

    def get(self, user_id: str) -> List[MemoryItem]:
        """Return all memory for a user (ordered by timestamp ascending)."""
        return sorted(self._store.get(user_id, []), key=lambda m: m.timestamp)

    def search(self, user_id: str, query: str, *, llm: Optional[str] = None) -> List[MemoryItem]:
        """Search a user's memory for items whose content contains the given query (case-insensitive).

        Optionally filter by the originating LLM.
        """
        query_lc = query.lower()
        results = [m for m in self.get(user_id) if query_lc in m.content.lower()]
        if llm is not None:
            results = [m for m in results if m.llm == llm]
        return results

    def delete(self, user_id: str) -> int:
        """Delete **all** memories for a user.

        Returns the number of items removed so callers can confirm deletion.
        """
        items = self._store.pop(user_id, [])
        return len(items)


# Global store instance the application can import
memory_store = MemoryStore() 