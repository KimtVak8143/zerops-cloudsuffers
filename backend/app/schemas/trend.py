from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.source import SourceRead


class TrendRead(BaseModel):
    id: int
    name: str
    slug: str
    category: str | None = None
    status: str | None = None
    tldr: str | None = None
    why_it_matters: str | None = None
    momentum: str | None = None
    tech_stack: List[str] | None = None
    related_trends: List[str] | None = None
    created_at: datetime
    updated_at: datetime
    sources: List[SourceRead] = []

    model_config = {"from_attributes": True}
