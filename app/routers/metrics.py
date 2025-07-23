from datetime import datetime, timezone

from fastapi import APIRouter

# Record the time when this module is first imported (startup time)
_start_time = datetime.now(timezone.utc)

router = APIRouter(prefix="/metrics", tags=["Info"])


@router.get("/uptime", summary="Server uptime in seconds")
async def get_uptime() -> dict[str, float]:
    """Return the number of seconds the API process has been running."""
    delta = datetime.now(timezone.utc) - _start_time
    return {"uptime_seconds": round(delta.total_seconds(), 2)} 