import time

from fastapi import APIRouter

from ..formatting import seconds_as_compact_label

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
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "uptime_label": seconds_as_compact_label(uptime),
        "version": "1.0.0",
    }


@router.get("/live", summary="Liveness probe")
async def health_live() -> dict[str, str]:
    """Minimal response for load balancers and orchestrators (e.g. Kubernetes liveness)."""
    return {"status": "alive"}