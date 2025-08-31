# NeuraVault MCP – Universal Memory Layer for AI

A lightweight FastAPI server that provides **persistent memory** for LLM-powered applications.  
Use it as an OpenAI-compatible plugin, call the REST API directly, or embed the in-process `MemoryStore` in your own Python code.

---

## ✨ Features

* **Store & retrieve memories** with a single HTTP call (`POST /memory` / `GET /memory/{user_id}`)
* **OpenAI Plugin Manifest** exposed at `/.well-known/ai-plugin.json` – add it to ChatGPT in seconds
* **Minimal dependencies** – FastAPI + Pydantic only
* **Drop-in Python API** (`from app.memory import memory_store`) for in-process usage
* Easily swap the in-memory backend for a real database or cache

---

## 🚀 Quick Start

```bash
# Clone repository & enter it
$ git clone https://github.com/your-org/mcp.git && cd mcp

# (Optional) create & activate a virtual environment
$ python -m venv .venv && source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the server (reload enabled when DEBUG=True)
$ uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>

---

## 🔌 Using as an OpenAI / ChatGPT Plugin

1. Start the server on a publicly accessible URL (e.g. via [ngrok](https://ngrok.com/)):
   ```bash
   ngrok http 8000
   ```
2. In ChatGPT → *Settings → Plugins* enable plugins and click *Develop your own plugin*.
3. Enter the **public URL** provided by ngrok. ChatGPT will automatically fetch:
   * `/.well-known/ai-plugin.json` – plugin manifest
   * `/openapi.json` – FastAPI-generated OpenAPI spec
4. ChatGPT can now call your `POST /memory` and `GET /memory/{user_id}` endpoints autonomously.

### Example Function Call from ChatGPT

```jsonc
{
  "name": "store_memory",
  "arguments": {
    "user_id": "alice",
    "llm": "gpt-4o",
    "content": "Alice said she loves sci-fi books."
  }
}
```

---

## 🛠️ REST API Reference

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET`  | `/health` | Health check – returns `{ "status": "ok" }` |
| `POST` | `/memory` | Store a new memory item |  
| `GET`  | `/memory/{user_id}` | Retrieve **all** memories for `user_id` |

### Request & Response Models

#### `POST /memory`
```jsonc
// Request body
{
  "user_id": "string",
  "llm": "string",            // e.g. "gpt-4o"
  "content": "string"         // Memory you want to store
}

// Successful response
{ "status": "stored" }
```

#### `GET /memory/{user_id}`  – `200 OK`
```jsonc
[
  {
    "user_id": "string",
    "llm": "string",
    "content": "string",
    "timestamp": "2024-01-01T12:00:00Z"
  }
]
```

---

## 🐍 In-Process Usage (Python)

```python
from app.memory import MemoryItem, memory_store

memory_store.add(
    MemoryItem(user_id="bob", llm="gpt-4o", content="Bob likes coffee.")
)

for item in memory_store.get("bob"):
    print(item.content)
```

---

## 🧩 Extending / Replacing the Backend

`MemoryStore` is deliberately simple. To use Redis, Postgres, or any other storage:

1. Create a subclass (or new implementation) that exposes the same `add()` and `get()` methods.
2. Replace the global `memory_store` in `app/memory.py` with your implementation.
3. (Optional) add dependency injection if you need per-request stores.

---

## ⚙️ Environment Variables

Variable | Default | Description
---------|---------|------------
`APP_NAME` | `NeuraVault MCP Server` | Title shown in docs
`DEBUG`    | `True` | Enables hot-reload & more verbose logging
`HOST`     | `0.0.0.0` | Host interface for Uvicorn
`PORT`     | `8000` | Port Uvicorn listens on

Create a local `.env` from the provided template:
```bash
cp env.example .env
```

---

## 📑 License

[MIT](LICENSE)
