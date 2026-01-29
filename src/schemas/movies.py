from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

try:
    from pydantic import ConfigDict  # Pydantic v2
except Exception:
    ConfigDict = None


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float = Field(..., ge=0, le=100)
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    if ConfigDict is not None:
        model_config = ConfigDict(from_attributes=True)
    else:
        class Config:
            orm_mode = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
