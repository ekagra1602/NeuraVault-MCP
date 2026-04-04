from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timezone
import time
import random
import hashlib
import base64
import binascii
from pydantic import BaseModel
from uuid import uuid4

from ..formatting import (
    collapse_whitespace,
    hex_encode_utf8,
    line_statistics,
    normalize_newlines,
    pad_center,
    pad_left,
    pad_right,
    reverse_word_order,
    strip_optional_prefix,
    strip_optional_suffix,
    truncate_plain,
    url_quote_utf8,
    url_unquote_utf8,
    utf8_byte_length,
)

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


@router.post("/unique-words", summary="Count unique words in text")
async def unique_words(input: TextInput) -> dict[str, object]:
    """
    Returns the number of unique whitespace-separated words (case-insensitive) and the set itself.
    """
    words = [w for w in input.text.split() if w]
    unique = sorted({w.lower() for w in words})
    return {"original": input.text, "unique_count": len(unique), "unique_words": unique}


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


@router.post("/swapcase", summary="Swap case of each character")
async def swapcase_text(input: TextInput) -> dict[str, str]:
    """
    Returns the original text and a version with each character's case swapped.
    """
    return {"original": input.text, "swapped": input.text.swapcase()}


@router.get("/modulo", summary="Compute modulo of two integers")
async def modulo(a: int, b: int) -> dict[str, int]:
    """
    Returns the remainder of a divided by b.
    Example: GET /utils/modulo?a=17&b=5
    """
    if b == 0:
        raise HTTPException(status_code=400, detail="Modulo by zero is not allowed")
    return {"a": a, "b": b, "remainder": a % b}


@router.get("/power", summary="Raise a number to a power")
async def power(base: float, exp: float) -> dict[str, float]:
    """
    Returns base raised to the power of exp.
    Example: GET /utils/power?base=2&exp=10
    """
    return {"base": base, "exp": exp, "result": base ** exp}


@router.post("/replace", summary="Replace occurrences in text")
async def replace_text(input: TextInput, old: str = "", new: str = "") -> dict[str, str]:
    """
    Replaces all occurrences of 'old' with 'new' in the input text.
    Example: POST /utils/replace?old=world&new=there  {"text":"hello world"}
    """
    return {"original": input.text, "old": old, "new": new, "result": input.text.replace(old, new)}


@router.post("/count-char", summary="Count occurrences of a character")
async def count_char(input: TextInput, char: str = "") -> dict[str, object]:
    """
    Returns how many times a given character appears in the input text.
    """
    if len(char) != 1:
        raise HTTPException(status_code=400, detail="char must be exactly one character")
    return {"original": input.text, "char": char, "count": input.text.count(char)}


@router.get("/abs", summary="Absolute value of a number")
async def absolute(n: float) -> dict[str, float]:
    """
    Returns the absolute value of the given number.
    Example: GET /utils/abs?n=-42.5
    """
    return {"n": n, "absolute": abs(n)}


@router.get("/min-max", summary="Return min and max of a list of numbers")
async def min_max(numbers: str) -> dict[str, object]:
    """
    Accepts a comma-separated string of numbers and returns the min and max.
    Example: GET /utils/min-max?numbers=3,1,4,1,5,9
    """
    try:
        vals = [float(n.strip()) for n in numbers.split(",") if n.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="All values must be valid numbers")
    if not vals:
        raise HTTPException(status_code=400, detail="At least one number is required")
    return {"numbers": vals, "min": min(vals), "max": max(vals)}


@router.post("/split", summary="Split text by a delimiter")
async def split_text(input: TextInput, delimiter: str = ",") -> dict[str, object]:
    """
    Splits input text by the given delimiter and returns the resulting list.
    Example: POST /utils/split?delimiter=- {"text":"a-b-c"}
    """
    parts = input.text.split(delimiter)
    return {"original": input.text, "delimiter": delimiter, "parts": parts, "count": len(parts)}


@router.post("/join", summary="Join a list of strings with a delimiter")
async def join_text(words: list[str], delimiter: str = ",") -> dict[str, object]:
    """
    Joins a list of strings using the given delimiter.
    Example: POST /utils/join?delimiter=- with body ["a","b","c"]
    """
    return {"words": words, "delimiter": delimiter, "result": delimiter.join(words)}


@router.post("/truncate", summary="Truncate text to a max length")
async def truncate_endpoint(
    input: TextInput,
    max_len: int = Query(80, ge=1, le=10_000, description="Maximum number of characters to keep"),
) -> dict[str, object]:
    out = truncate_plain(input.text, max_len)
    return {"original": input.text, "max_len": max_len, "truncated": out}


@router.post("/collapse-space", summary="Collapse internal whitespace to single spaces")
async def collapse_space_endpoint(input: TextInput) -> dict[str, str]:
    return {"original": input.text, "collapsed": collapse_whitespace(input.text)}


@router.post("/line-stats", summary="Count lines and non-blank lines in text")
async def line_stats_endpoint(input: TextInput) -> dict[str, object]:
    stats = line_statistics(input.text)
    return {"original": input.text, **stats}


@router.post("/normalize-newlines", summary="Normalize line endings to LF")
async def normalize_newlines_endpoint(input: TextInput) -> dict[str, str]:
    return {"original": input.text, "normalized": normalize_newlines(input.text)}


@router.post("/utf8-byte-length", summary="UTF-8 encoded byte length of text")
async def utf8_byte_length_endpoint(input: TextInput) -> dict[str, object]:
    return {
        "original": input.text,
        "char_length": len(input.text),
        "utf8_byte_length": utf8_byte_length(input.text),
    }


@router.post("/reverse-word-order", summary="Reverse order of whitespace-separated words")
async def reverse_word_order_endpoint(input: TextInput) -> dict[str, str]:
    return {"original": input.text, "reversed_words": reverse_word_order(input.text)}


@router.post("/utf8-hex", summary="Hex-encode UTF-8 bytes of text")
async def utf8_hex_endpoint(input: TextInput) -> dict[str, str]:
    return {"original": input.text, "hex": hex_encode_utf8(input.text)}


@router.post("/pad-left", summary="Left-pad text to a minimum width")
async def pad_left_endpoint(
    input: TextInput,
    width: int = Query(..., ge=1, le=1_000_000, description="Minimum resulting string length"),
    fill: str = Query(" ", description="Single character to repeat for padding", min_length=1, max_length=1),
) -> dict[str, object]:
    return {
        "original": input.text,
        "width": width,
        "fill": fill,
        "padded": pad_left(input.text, width, fill),
    }


@router.post("/pad-right", summary="Right-pad text to a minimum width")
async def pad_right_endpoint(
    input: TextInput,
    width: int = Query(..., ge=1, le=1_000_000, description="Minimum resulting string length"),
    fill: str = Query(" ", description="Single character to repeat for padding", min_length=1, max_length=1),
) -> dict[str, object]:
    return {
        "original": input.text,
        "width": width,
        "fill": fill,
        "padded": pad_right(input.text, width, fill),
    }


@router.post("/strip-prefix", summary="Remove leading prefix if present")
async def strip_prefix_endpoint(
    input: TextInput,
    prefix: str = Query("", description="Prefix to remove once when it matches the start"),
) -> dict[str, str]:
    return {
        "original": input.text,
        "prefix": prefix,
        "stripped": strip_optional_prefix(input.text, prefix),
    }


@router.post("/strip-suffix", summary="Remove trailing suffix if present")
async def strip_suffix_endpoint(
    input: TextInput,
    suffix: str = Query("", description="Suffix to remove once when it matches the end"),
) -> dict[str, str]:
    return {
        "original": input.text,
        "suffix": suffix,
        "stripped": strip_optional_suffix(input.text, suffix),
    }


@router.post("/pad-center", summary="Center-pad text to a minimum width")
async def pad_center_endpoint(
    input: TextInput,
    width: int = Query(..., ge=1, le=1_000_000, description="Minimum resulting string length"),
    fill: str = Query(" ", description="Single character to repeat for padding", min_length=1, max_length=1),
) -> dict[str, object]:
    return {
        "original": input.text,
        "width": width,
        "fill": fill,
        "padded": pad_center(input.text, width, fill),
    }


@router.post("/url-quote", summary="Percent-encode text for URLs (UTF-8)")
async def url_quote_endpoint(
    input: TextInput,
    safe: str = Query(
        "",
        description="Characters that must not be encoded (e.g. use /.-_ for path-like text)",
    ),
) -> dict[str, str]:
    return {
        "original": input.text,
        "safe": safe,
        "quoted": url_quote_utf8(input.text, safe),
    }


@router.post("/url-unquote", summary="Decode percent-encoded URL component (UTF-8, strict)")
async def url_unquote_endpoint(input: TextInput) -> dict[str, str]:
    try:
        decoded = url_unquote_utf8(input.text)
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid percent-encoding or not valid UTF-8 after decoding",
        )
    return {"original": input.text, "decoded": decoded}


@router.get("/ping", summary="Simple ping endpoint")
async def ping() -> dict[str, str]:
    """
    Returns a simple pong response to verify the utils router is reachable.
    """
    return {"message": "pong"}