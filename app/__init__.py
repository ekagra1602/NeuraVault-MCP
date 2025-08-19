import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

__all__ = [
    "get_random_greeting",
    "get_random_color",
    "generate_mcp_context",
    "get_user_memory_counts",
    "get_memory_stats",
    "get_recent_memories",
    "prune_memories_before",
    "export_user_memories",
    "truncate_user_memories",
    "search_user_memories",
    "get_memories_since",
    "deduplicate_user_memories",
    "merge_user_memories",
    "get_user_memory_by_llm",
    "bulk_add_memories",
    "validate_memory_store",
    "get_oldest_memories",
    "get_memories_by_position",
]


def get_random_greeting() -> str:
    """Return a random greeting from a predefined list."""
    greetings = [
        "Hello!",
        "Hi there!",
        "Greetings!",
        "Howdy!",
        "Hey!",
        "Welcome!",
    ]
    return random.choice(greetings)


def get_random_color() -> str:
    """Return a random color name from a predefined list."""
    colors = [
        "Red",
        "Blue",
        "Green",
        "Yellow",
        "Purple",
        "Orange",
        "Pink",
        "Black",
        "White",
        "Gray",
    ]
    return random.choice(colors)


def generate_mcp_context(user_id: str | None = None) -> Dict[str, Any]:
    """Generate sample context data for Model Context Protocol (MCP) testing."""
    if user_id is None:
        user_id = f"user_{random.randint(1000, 9999)}"

    context_types = [
        "conversation_history",
        "user_preferences",
        "system_context",
        "session_data",
        "model_configuration",
    ]

    sample_contexts = {
        "conversation_history": [
            "Previous discussion about API design patterns",
            "User asked about best practices for error handling",
            "Conversation about database optimization strategies",
        ],
        "user_preferences": [
            "User prefers detailed explanations with code examples",
            "User likes to see multiple approaches to solving problems",
            "User prefers concise responses for quick questions",
        ],
        "system_context": [
            "Current session started 2 hours ago",
            "User is working on a Python FastAPI project",
            "Previous context includes memory management discussions",
        ],
        "session_data": [
            "Session ID: mcp_session_2024_001",
            "Active tools: file_reader, code_analyzer, memory_store",
            "Current working directory: /projects/mcp",
        ],
        "model_configuration": [
            "Model: gpt-4o with temperature 0.7",
            "Max tokens: 4000",
            "Context window: 128k tokens",
        ],
    }

    context_type = random.choice(context_types)

    return {
        "user_id": user_id,
        "context_type": context_type,
        "content": random.choice(sample_contexts[context_type]),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "protocol_version": "1.0",
    }


def get_user_memory_counts() -> Dict[str, int]:
    """Return a mapping of user IDs to the number of memory items stored in the global MemoryStore."""
    from .memory import memory_store  # Local import to avoid circular dependency

    return {user_id: len(items) for user_id, items in memory_store._store.items()}


def get_memory_stats(user_id: str) -> Dict[str, Any]:
    """Return total, first_timestamp, and last_timestamp for the user's stored memories.

    Equivalent to calling the `/memory/{user_id}/stats` API route, but usable in-process.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return {"total": 0, "first_timestamp": None, "last_timestamp": None}

    return {
        "total": len(items),
        "first_timestamp": items[0].timestamp,
        "last_timestamp": items[-1].timestamp,
    }


def get_recent_memories(user_id: str, limit: int = 5):
    """Return up to `limit` most recent MemoryItem objects for the given user.

    The items are returned in descending timestamp order (most recent first).
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return []

    # `memory_store.get` returns items sorted ascending by timestamp.
    return items[-limit:][::-1]


def prune_memories_before(user_id: str, cutoff: datetime) -> int:
    """Delete all memories for `user_id` that were created **before** the given `cutoff` timestamp.

    Returns the number of items removed. If the user has no memories or none match the cutoff, zero is returned.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    original_items = memory_store.get(user_id)
    if not original_items:
        return 0

    remaining = [m for m in original_items if m.timestamp >= cutoff]
    removed_count = len(original_items) - len(remaining)

    # Update store with remaining items (or remove key entirely if now empty)
    if remaining:
        memory_store._store[user_id] = remaining
    else:
        memory_store._store.pop(user_id, None)

    return removed_count


def export_user_memories(user_id: str, *, as_json: bool = False):
    """Export all memories for a user.

    If `as_json` is True, returns a JSON string; otherwise returns a list of dicts.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    data = [item.dict() for item in items]
    if as_json:
        return json.dumps(data, default=str)
    return data


def truncate_user_memories(user_id: str, keep_last: int = 100) -> int:
    """Keep only the last `keep_last` memories for a user; delete older ones.

    Returns the number of items removed. Uses the in-memory store ordering semantics
    (older first) to safely slice the tail.
    """
    if keep_last <= 0:
        # If caller passes 0 or negative, remove all
        from .memory import memory_store
        removed = len(memory_store.get(user_id))
        memory_store._store.pop(user_id, None)
        return removed

    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if len(items) <= keep_last:
        return 0

    # Keep last N items (most recent), drop the rest
    kept = items[-keep_last:]
    removed_count = len(items) - len(kept)
    memory_store._store[user_id] = kept
    return removed_count


def search_user_memories(user_id: str, query: str, llm: str | None = None):
    """In-process convenience wrapper over MemoryStore.search for the given user.

    Returns a list of MemoryItem objects matching the substring `query`. If `llm`
    is provided, results are filtered to that LLM.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    return memory_store.search(user_id, query, llm=llm)


def get_memories_since(user_id: str, since: datetime):
    """Return all memories for `user_id` with timestamp >= `since` (ascending order)."""
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return []
    return [m for m in items if m.timestamp >= since]


def deduplicate_user_memories(user_id: str) -> int:
    """Remove exact-duplicate memory contents for a user (case-insensitive), keeping the most recent.

    Returns the number of items removed.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return 0

    seen_lower_content: set[str] = set()
    deduped: list = []

    # Iterate from newest to oldest to keep most recent duplicates
    for item in reversed(items):
        content_key = item.content.strip().lower()
        if content_key in seen_lower_content:
            continue
        seen_lower_content.add(content_key)
        deduped.append(item)

    # deduped currently holds items newest->oldest; reverse back to ascending order
    deduped.reverse()

    removed = len(items) - len(deduped)
    if removed > 0:
        memory_store._store[user_id] = deduped
    return removed


def merge_user_memories(source_user_id: str, target_user_id: str, *, deduplicate: bool = False) -> int:
    """Move all memories from `source_user_id` into `target_user_id`.

    Returns the number of items moved. If `deduplicate` is True, removes exact
    duplicate contents on the target after merging (keeping most recent).
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    if source_user_id == target_user_id:
        return 0

    source_items = memory_store.get(source_user_id)
    if not source_items:
        # Nothing to move
        memory_store._store.pop(source_user_id, None)
        return 0

    target_items = memory_store.get(target_user_id)

    # Merge, then sort ascending by timestamp to preserve store invariant
    merged = sorted([*target_items, *source_items], key=lambda m: m.timestamp)
    moved = len(source_items)

    memory_store._store[target_user_id] = merged
    memory_store._store.pop(source_user_id, None)

    if deduplicate:
        # Reuse existing helper to dedupe target user's items
        try:
            removed = deduplicate_user_memories(target_user_id)  # type: ignore[name-defined]
        except NameError:
            # Fallback: simple inline dedupe if helper not found at import time
            seen_lower_content: set[str] = set()
            deduped: list = []
            for item in reversed(merged):
                content_key = item.content.strip().lower()
                if content_key in seen_lower_content:
                    continue
                seen_lower_content.add(content_key)
                deduped.append(item)
            deduped.reverse()
            memory_store._store[target_user_id] = deduped

    return moved


def get_user_memory_by_llm(user_id: str) -> Dict[str, int]:
    """Return a mapping of LLM model names to the count of memories for that user.

    Useful for analytics or understanding which models generated the most context.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return {}

    llm_counts: Dict[str, int] = {}
    for item in items:
        llm_counts[item.llm] = llm_counts.get(item.llm, 0) + 1
    
    return llm_counts


def bulk_add_memories(memories: List[Dict[str, Any]]) -> int:
    """Add multiple memory items from a list of dicts in one operation.
    
    Each dict should contain 'user_id', 'llm', and 'content' keys.
    Returns the number of items successfully added.
    """
    from .memory import MemoryItem, memory_store  # Local import to avoid circular dependency
    
    added_count = 0
    for mem_data in memories:
        try:
            # Create MemoryItem - timestamp will be auto-generated if not provided
            item = MemoryItem(**mem_data)
            memory_store.add(item)
            added_count += 1
        except (TypeError, ValueError):
            # Skip invalid entries
            continue
    
    return added_count


def validate_memory_store() -> Dict[str, Any]:
    """Run basic validation checks on the memory store and return a report.
    
    Checks for duplicate timestamps, invalid data, and consistency issues.
    """
    from .memory import memory_store  # Local import to avoid circular dependency
    
    report = {
        "total_users": 0,
        "total_memories": 0,
        "duplicate_timestamps": 0,
        "invalid_entries": 0,
        "users_with_issues": [],
        "timestamp_order_violations": 0,
    }
    
    for user_id, items in memory_store._store.items():
        report["total_users"] += 1
        report["total_memories"] += len(items)
        
        user_issues = []
        timestamps = []
        
        for item in items:
            # Check for required fields
            if not hasattr(item, 'user_id') or not hasattr(item, 'llm') or not hasattr(item, 'content'):
                report["invalid_entries"] += 1
                user_issues.append("missing_required_fields")
            
            if hasattr(item, 'timestamp'):
                timestamps.append(item.timestamp)
        
        # Check timestamp ordering (should be ascending)
        if timestamps:
            sorted_timestamps = sorted(timestamps)
            if timestamps != sorted_timestamps:
                report["timestamp_order_violations"] += 1
                user_issues.append("timestamp_order_violation")
        
        # Check for duplicate timestamps
        if len(timestamps) != len(set(timestamps)):
            duplicate_count = len(timestamps) - len(set(timestamps))
            report["duplicate_timestamps"] += duplicate_count
            user_issues.append("duplicate_timestamps")
        
        if user_issues:
            report["users_with_issues"].append({"user_id": user_id, "issues": user_issues})
    
    return report


def get_oldest_memories(user_id: str, limit: int = 5):
    """Return up to `limit` oldest MemoryItem objects for the given user.

    The items are returned in ascending timestamp order (oldest first).
    Complements get_recent_memories() for accessing historical context.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return []

    # `memory_store.get` returns items sorted ascending by timestamp.
    # Return first N items (oldest)
    return items[:limit]


def get_memories_by_position(user_id: str, start: int = 0, end: int | None = None):
    """Return memories for a user by position/index range in their timeline.

    Args:
        user_id: The user whose memories to retrieve
        start: Starting index (inclusive, 0-based)
        end: Ending index (exclusive), or None for rest of memories

    Returns memories in ascending timestamp order (chronological).
    Useful for pagination or accessing specific segments of memory history.
    """
    from .memory import memory_store  # Local import to avoid circular dependency

    items = memory_store.get(user_id)
    if not items:
        return []

    # Handle negative indices and bounds
    if start < 0:
        start = max(0, len(items) + start)
    
    if end is None:
        return items[start:]
    else:
        if end < 0:
            end = max(0, len(items) + end)
        return items[start:end]
