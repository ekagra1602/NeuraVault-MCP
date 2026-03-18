import time

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

_start_time = time.time()


@router.get("/", summary="Health check")
async def health_check() -> dict[str, str]:
    """Simple health check endpoint to verify that the service is running."""
    return {"status": "ok"}


@router.get("/details", summary="Detailed health check")
async def health_details() -> dict[str, object]:
    """Returns server uptime in seconds and the API version."""
    uptime = round(time.time() - _start_time, 2)
    return {"status": "ok", "uptime_seconds": uptime, "version": "1.0.0"}