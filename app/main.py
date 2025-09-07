from fastapi import FastAPI, Request

from .config import get_settings
from .routers import health, memory

from dotenv import load_dotenv
import time

load_dotenv()

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    # Include routers
    app.include_router(health.router)
    app.include_router(memory.router)

    # Add per-request latency header so clients can see server-side processing time
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{duration:.4f}s"
        return response

    # Expose OpenAI plugin manifest so the server can be registered as a ChatGPT / LLM plugin
    @app.get("/.well-known/ai-plugin.json", include_in_schema=False)
    async def plugin_manifest() -> dict[str, object]:
        """Return the plugin manifest so compatible LLMs (e.g. ChatGPT) can discover the API."""
        return {
            "schema_version": "v1",
            "name_for_human": "NeuraVault MCP Memory Plugin",
            "name_for_model": "mcp_memory",
            "description_for_human": "Store and retrieve user memories to provide long-term context to LLM applications.",
            "description_for_model": (
                "Plugin for managing persistent memories. "
                "Use `POST /memory` to add a memory (requires `user_id`, `llm`, `content`). "
                "Use `GET /memory/{user_id}` to fetch all memories for a user. "
                "Use `GET /memory/{user_id}/relevant?prompt=...&k=5` to fetch the top-k relevant memories for a prompt. "
                "Use `GET /memory/{user_id}/relevant_diverse?prompt=...&k=5` to fetch relevant and diverse memories using MMR. "
                "Use `GET /memory/{user_id}/relevant_pack?prompt=...&budget_chars=2000` to fetch packed context text and items within a size budget."
            ),
            "auth": {"type": "none"},
            "api": {
                "type": "openapi",
                "url": f"http://{settings.host}:{settings.port}/openapi.json",
            },
            "logo_url": None,
            "contact_email": "support@example.com",
            "legal_info_url": "https://github.com/ekagra1602/NeuraVault-MCP#license",
        }

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    ) 