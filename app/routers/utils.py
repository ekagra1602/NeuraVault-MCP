from fastapi import APIRouter
from pydantic import BaseModel

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
