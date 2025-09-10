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


@router.get(
    "/{user_id}/recent",
    summary="Retrieve the most recent k memory items for a user",
    response_model=List[MemoryItem],
)
async def recent_memory(
    user_id: str,
    k: int = Query(5, ge=1, le=50, description="Number of recent items to return"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
) -> List[MemoryItem]:
    """Return the most recent k memory items for a user, optionally filtered by LLM."""
    return memory_store.recent(user_id, llm=llm, k=k)


# New: search endpoint


@router.get("/{user_id}/search", summary="Search memory for a user", response_model=List[MemoryItem])
async def search_memory(
    user_id: str,
    q: str = Query(..., description="Search term (case-insensitive substring match)"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
) -> List[MemoryItem]:
    """Search within a user's memory items and optionally filter by LLM."""
    return memory_store.search(user_id, q, llm=llm)


# Relevant endpoint


@router.get(
    "/{user_id}/relevant",
    summary="Retrieve top-k relevant memories for a prompt",
    response_model=List[MemoryItem],
)
async def relevant_memory(
    user_id: str,
    prompt: str = Query(..., description="The prompt/turn to retrieve context for"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
    k: int = Query(5, ge=1, le=50, description="Max number of items to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score to include"),
) -> List[MemoryItem]:
    """Return the k most relevant memories for the given prompt using lightweight TF-IDF similarity."""
    return memory_store.relevant(user_id, prompt, llm=llm, k=k, min_score=min_score)


@router.get(
    "/{user_id}/relevant_diverse",
    summary="Retrieve top-k relevant and diverse memories for a prompt (MMR)",
    response_model=List[MemoryItem],
)
async def relevant_diverse_memory(
    user_id: str,
    prompt: str = Query(..., description="The prompt/turn to retrieve context for"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
    k: int = Query(5, ge=1, le=50, description="Max number of items to return"),
    lambda_mult: float = Query(0.5, ge=0.0, le=1.0, description="Relevance-diversity tradeoff (1=relevance)"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score to include"),
) -> List[MemoryItem]:
    """Return the k most relevant and diverse memories using Maximal Marginal Relevance (MMR)."""
    return memory_store.relevant_diverse(
        user_id,
        prompt,
        llm=llm,
        k=k,
        lambda_mult=lambda_mult,
        min_score=min_score,
    )


@router.get(
    "/{user_id}/relevant_time_decay",
    summary="Retrieve top-k relevant memories with time decay favoring recent items",
    response_model=List[MemoryItem],
)
async def relevant_time_decay_memory(
    user_id: str,
    prompt: str = Query(..., description="The prompt/turn to retrieve context for"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
    k: int = Query(5, ge=1, le=50, description="Max number of items to return"),
    half_life_hours: float = Query(24.0, ge=0.01, le=24*365.0, description="Half-life hours for time decay"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score to include"),
) -> List[MemoryItem]:
    """Return the k most relevant memories applying exponential time decay by recency."""
    return memory_store.relevant_time_decay(
        user_id,
        prompt,
        llm=llm,
        k=k,
        half_life_hours=half_life_hours,
        min_score=min_score,
    )

class PackedResponse(BaseModel):
    items: List[MemoryItem]
    packed_text: str


@router.get(
    "/{user_id}/relevant_pack",
    summary="Retrieve relevant memories packed into a single string under a budget",
    response_model=PackedResponse,
)
async def relevant_pack_memory(
    user_id: str,
    prompt: str = Query(..., description="The prompt/turn to retrieve context for"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
    k: int = Query(10, ge=1, le=50, description="Max number of items to include"),
    budget_chars: int = Query(2000, ge=1, le=20000, description="Character budget for packed text"),
    strategy: str = Query("relevant", description='Scoring strategy: "relevant" or "mmr"'),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score to include"),
    lambda_mult: float = Query(0.5, ge=0.0, le=1.0, description="MMR tradeoff (only used with strategy=mmr)"),
) -> PackedResponse:
    """Return packed relevant memories along with the combined text, under a size budget."""
    items, packed_text = memory_store.relevant_pack(
        user_id,
        prompt,
        llm=llm,
        k=k,
        budget_chars=budget_chars,
        strategy=strategy,
        min_score=min_score,
        lambda_mult=lambda_mult,
    )
    return PackedResponse(items=items, packed_text=packed_text)


@router.get(
    "/{user_id}/relevant_window",
    summary="Retrieve top-k relevant memories within a recent window (count/hours)",
    response_model=List[MemoryItem],
)
async def relevant_window_memory(
    user_id: str,
    prompt: str = Query(..., description="The prompt/turn to retrieve context for"),
    llm: Optional[str] = Query(None, description="Filter by LLM name"),
    k: int = Query(5, ge=1, le=50, description="Max number of items to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score to include"),
    window_count: Optional[int] = Query(None, ge=1, le=1000, description="Consider only the most recent N items"),
    window_hours: Optional[float] = Query(None, ge=0.0, le=24*365.0, description="Consider only items within the past hours"),
) -> List[MemoryItem]:
    """Return relevant memories restricted to a recent window by time and/or count."""
    return memory_store.relevant_window(
        user_id,
        prompt,
        llm=llm,
        k=k,
        min_score=min_score,
        window_count=window_count,
        window_hours=window_hours,
    )


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