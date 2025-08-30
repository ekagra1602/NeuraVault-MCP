# Memora MCP - Development Guide

A universal memory layer for AI models supporting OpenAI, Gemini, Claude, Grok, and any LLM with context protocol support.

## 🚀 Quick Start

### One-Command Setup
```bash
./setup.sh
```

### Manual Setup

#### Backend (Python FastAPI)
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload
```

#### Frontend (React + TypeScript)
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## 📁 Project Structure

```
mcp/
├── app/                    # Python FastAPI backend
│   ├── __init__.py        # Memory management utilities
│   ├── main.py            # FastAPI app and routes
│   ├── memory.py          # Memory store implementation
│   ├── config.py          # Configuration management
│   └── routers/           # API route modules
├── frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   └── lib/          # Utilities
│   ├── package.json      # Node.js dependencies
│   └── vite.config.ts    # Vite configuration
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── setup.sh              # Project setup script
├── start-backend.sh      # Backend startup script
└── start-frontend.sh     # Frontend startup script
```

## 🛠️ Development Scripts

| Script | Purpose |
|--------|---------|
| `./setup.sh` | Complete project setup (backend + frontend) |
| `./start-backend.sh` | Start FastAPI server |
| `./start-frontend.sh` | Start React development server |

## 🌐 URLs

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173  
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
Copy `env.example` to `.env` and configure:

```bash
cp env.example .env
```

### Backend Configuration
- **Host**: `0.0.0.0` (configurable via `HOST` env var)
- **Port**: `8000` (configurable via `PORT` env var)
- **Debug**: `True` in development

### Frontend Configuration
- **Vite Dev Server**: Port 5173
- **API Proxy**: `/api` routes proxy to backend
- **Hot Reload**: Enabled in development

## 📦 Dependencies

### Backend (Python)
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-dotenv**: Environment management

### Frontend (React)
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Framer Motion**: Animations
- **Lucide React**: Icons

## 🚫 Git Ignore

The `.gitignore` includes:
- `node_modules/` - Frontend dependencies
- `__pycache__/` - Python cache
- `.venv/` - Virtual environment
- `dist/` - Build outputs
- `.env` - Environment variables
- Editor and OS files

## 🧪 Testing

### Backend Testing
```bash
source .venv/bin/activate
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 API Usage Examples

### Store Memory
```bash
curl -X POST "http://localhost:8000/memory" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "alice",
    "llm": "gpt-4o",
    "content": "Alice prefers concise explanations"
  }'
```

### Retrieve Memories
```bash
curl "http://localhost:8000/memory/alice"
```

### Multi-LLM Context
```python
from app.memory import MemoryItem, memory_store

# Store from different models
models = ["gpt-4o", "claude-3-opus", "gemini-pro", "grok-1"]
for model in models:
    memory_store.add(MemoryItem(
        user_id="bob",
        llm=model,
        content=f"User preference learned via {model}"
    ))

# Retrieve all cross-model memories
memories = memory_store.get("bob")
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Python virtual environment issues**
   ```bash
   # Recreate virtual environment
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Node modules issues**
   ```bash
   # Clear and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

## 🚀 Production Deployment

### Backend
```bash
# Production server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend
```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or similar
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
