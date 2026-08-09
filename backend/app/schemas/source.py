from datetime import datetime

from pydantic import BaseModel, HttpUrl


class SourceRead(BaseModel):
    id: int
    title: str
    url: HttpUrl
    source_type: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
