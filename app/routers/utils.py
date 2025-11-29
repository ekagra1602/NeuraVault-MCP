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
