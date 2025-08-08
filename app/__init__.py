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
