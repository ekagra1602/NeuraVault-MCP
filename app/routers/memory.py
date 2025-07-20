from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..memory import MemoryItem, memory_store

router = APIRouter(prefix="/memory", tags=["Memory"])


class StoreMemoryRequest(BaseModel):
    user_id: str
    llm: str
    content: str
    
class MemoryStats(BaseModel):
    total: int
    first_timestamp: Optional[datetime]
    last_timestamp: Optional[datetime]


@router.post("/", summary="Store a new memory item")
async def store_memory(request: StoreMemoryRequest) -> dict[str, str]:
    """Persist a new memory entry for a given user and LLM."""
    item = MemoryItem(**request.dict())
    memory_store.add(item)
    return {"status": "stored"}


@router.get("/{user_id}", summary="Retrieve all memory for a user", response_model=List[MemoryItem])
async def read_memory(user_id: str) -> List[MemoryItem]:
    """Get the entire memory timeline for a user."""
    return memory_store.get(user_id)


# New: search endpoint


@router.get("/{user_id}/search", summary="Search memory for a user", response_model=List[MemoryItem])
async def search_memory(
    user_id: str,
    q: str = Query(..., description="Search term (case-insensitive substring match)"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
) -> List[MemoryItem]:
    """Search within a user's memory items and optionally filter by LLM."""
    return memory_store.search(user_id, q, llm=llm)


# Stats endpoint


@router.get("/{user_id}/stats", summary="Get memory stats for a user", response_model=MemoryStats)
async def memory_stats(user_id: str) -> MemoryStats:
    """Return total number of items and earliest/latest timestamps."""
    items = memory_store.get(user_id)
    if not items:
        return MemoryStats(total=0, first_timestamp=None, last_timestamp=None)

    return MemoryStats(
        total=len(items),
        first_timestamp=items[0].timestamp,
        last_timestamp=items[-1].timestamp,
    )


# Delete endpoint


class DeleteMemoryResponse(BaseModel):
    deleted: int


@router.delete("/{user_id}", summary="Delete all memories for a user", response_model=DeleteMemoryResponse)
async def delete_memory(user_id: str) -> DeleteMemoryResponse:
    """Remove every memory item for the specified user and return the number deleted."""
    removed = memory_store.delete(user_id)
    return DeleteMemoryResponse(deleted=removed) 