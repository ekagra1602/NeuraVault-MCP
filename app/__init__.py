import random
from datetime import datetime

__all__ = [
    "get_random_greeting",
    "get_random_color",
    "generate_mcp_context",
    "get_user_memory_counts",
]


def get_random_greeting():
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


def get_random_color():
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


def generate_mcp_context(user_id: str | None = None):
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


def get_user_memory_counts() -> dict[str, int]:
    """Return a mapping of user IDs to the number of memory items stored in the global MemoryStore."""
    from .memory import memory_store  # Local import to avoid circular dependency

    return {user_id: len(items) for user_id, items in memory_store._store.items()} 