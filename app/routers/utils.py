from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import time
import random
import hashlib
import base64
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}},
)

class TextInput(BaseModel):
    text: str

@router.post("/text-stats")
async def get_text_stats(input: TextInput):
    """
    Returns statistics for the given text: character count and word count.
    """
    return {
        "char_count": len(input.text),
        "word_count": len(input.text.split())
    }


@router.get("/add", summary="Add two numbers")
async def add(a: float, b: float) -> dict[str, float]:
    """
    Returns the sum of two numbers provided as query parameters.
    Example: GET /utils/add?a=1.5&b=2
    """
    return {"a": a, "b": b, "sum": a + b}


@router.get("/multiply", summary="Multiply two numbers")
async def multiply(a: float, b: float) -> dict[str, float]:
    """
    Returns the product of two numbers provided as query parameters.
    Example: GET /utils/multiply?a=3&b=4
    """
    return {"a": a, "b": b, "product": a * b}


@router.get("/divide", summary="Divide two numbers")
async def divide(a: float, b: float) -> dict[str, float]:
    """
    Returns the quotient of two numbers provided as query parameters.
    Example: GET /utils/divide?a=10&b=2
    """
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return {"a": a, "b": b, "quotient": a / b}


@router.get("/timestamp", summary="Get current server time")
async def timestamp() -> dict[str, object]:
    """
    Returns the current server timestamp in ISO-8601 and epoch milliseconds.
    Example: GET /utils/timestamp
    """
    now = datetime.now(timezone.utc)
    return {
        "iso": now.isoformat(),
        "epoch_ms": int(time.time() * 1000),
    }

@router.post("/reverse", summary="Reverse a string")
async def reverse_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its reversed version.
    """
    return {"original": input.text, "reversed": input.text[::-1]}

@router.post("/uppercase", summary="Uppercase a string")
async def uppercase_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its uppercase version.
    """
    return {"original": input.text, "uppercased": input.text.upper()}


@router.get("/uuid", summary="Generate a UUID v4")
async def generate_uuid() -> dict[str, str]:
    """
    Returns a newly generated UUID v4 string.
    Example: GET /utils/uuid
    """
    return {"uuid": str(uuid4())}


@router.get("/random-int", summary="Generate a random integer in [min, max]")
async def random_int(min: int = 0, max: int = 100) -> dict[str, int]:
    """
    Returns a random integer between min and max (inclusive).
    Example: GET /utils/random-int?min=10&max=20
    """
    if min > max:
        raise HTTPException(status_code=400, detail="min must be <= max")
    value = random.randint(min, max)
    return {"min": min, "max": max, "value": value}


@router.post("/sha256", summary="Compute SHA-256 hash of text")
async def sha256_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its SHA-256 hex digest.
    """
    digest = hashlib.sha256(input.text.encode("utf-8")).hexdigest()
    return {"original": input.text, "sha256": digest}


@router.post("/base64-encode", summary="Base64-encode a string")
async def base64_encode(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its Base64-encoded representation.
    """
    encoded = base64.b64encode(input.text.encode("utf-8")).decode("ascii")
    return {"original": input.text, "base64": encoded}
