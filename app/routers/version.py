from fastapi import APIRouter

from ..config import get_settings

router = APIRouter(prefix="/version", tags=["Info"])


@router.get("/", summary="Application version")
async def get_version() -> dict[str, str]:
    """Return the running application version from settings."""
    settings = get_settings()
    return {"version": settings.app_version} 