from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import time
import random
import hashlib
import base64
import binascii
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

@router.post("/lowercase", summary="Lowercase a string")
async def lowercase_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its lowercase version.
    """
    return {"original": input.text, "lowercased": input.text.lower()}

@router.post("/titlecase", summary="Titlecase a string")
async def titlecase_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and its titlecased version.
    """
    return {"original": input.text, "titlecased": input.text.title()}


@router.post("/trim", summary="Trim whitespace from a string")
async def trim_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and a trimmed version without leading/trailing whitespace.
    """
    return {"original": input.text, "trimmed": input.text.strip()}


@router.post("/first-last", summary="Get first and last character")
async def first_last_text(input: TextInput) -> dict[str, object]:
    """
    Returns first and last characters for non-empty text, otherwise null values.
    """
    if not input.text:
        return {"original": input.text, "first": None, "last": None}
    return {"original": input.text, "first": input.text[0], "last": input.text[-1]}


@router.post("/repeat", summary="Repeat a string N times")
async def repeat_text(input: TextInput, times: int = 2) -> dict[str, object]:
    """
    Returns the original text repeated N times.
    """
    if times < 1 or times > 20:
        raise HTTPException(status_code=400, detail="times must be between 1 and 20")
    return {"original": input.text, "times": times, "repeated": input.text * times}


@router.post("/contains", summary="Check if text contains a substring")
async def contains_text(input: TextInput, needle: str) -> dict[str, object]:
    """
    Returns whether the input text contains the provided substring.
    """
    return {"original": input.text, "needle": needle, "contains": needle in input.text}


@router.post("/is-palindrome", summary="Check if text is a palindrome")
async def is_palindrome_text(input: TextInput) -> dict[str, object]:
    """
    Returns whether the text is a palindrome, ignoring case and non-alphanumeric chars.
    """
    normalized = "".join(ch.lower() for ch in input.text if ch.isalnum())
    return {"original": input.text, "normalized": normalized, "is_palindrome": normalized == normalized[::-1]}


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


@router.post("/base64-decode", summary="Base64-decode a string")
async def base64_decode(input: TextInput) -> dict[str, str]:
    """
    Returns the original Base64 text and its UTF-8 decoded representation.
    """
    try:
        decoded_bytes = base64.b64decode(input.text.encode("ascii"), validate=True)
        decoded_text = decoded_bytes.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid Base64 input")
    return {"original": input.text, "decoded": decoded_text}


@router.post("/capitalize", summary="Capitalize first character only")
async def capitalize_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and a version with only the first character capitalized.
    """
    return {"original": input.text, "capitalized": input.text.capitalize()}


@router.get("/ping", summary="Simple ping endpoint")
async def ping() -> dict[str, str]:
    """
    Returns a simple pong response to verify the utils router is reachable.
    """
    return {"message": "pong"}