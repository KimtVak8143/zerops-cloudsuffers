from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_async_db
from app.models.trend import Trend
from app.schemas.trend import TrendRead

router = APIRouter()


@router.get("", response_model=List[TrendRead])
async def list_trends(
    category: Optional[str] = Query(None, description="Filter trends by category"),
    status: Optional[str] = Query(None, description="Filter trends by adoption or momentum status"),
    search: Optional[str] = Query(None, description="Search by trend name or summary"),
    db: AsyncSession = Depends(get_async_db),
) -> List[TrendRead]:
    stmt = select(Trend).options(selectinload(Trend.sources)).order_by(Trend.created_at.desc())

    if category:
        stmt = stmt.filter(Trend.category.ilike(f"%{category}%"))
    if status:
        stmt = stmt.filter(Trend.status.ilike(f"%{status}%"))
    if search:
        stmt = stmt.filter(
            or_(
                Trend.name.ilike(f"%{search}%"),
                Trend.tldr.ilike(f"%{search}%"),
                Trend.why_it_matters.ilike(f"%{search}%"),
            )
        )

    result = await db.execute(stmt)
    return result.scalars().unique().all()


@router.get("/{slug}", response_model=TrendRead)
async def get_trend(slug: str, db: AsyncSession = Depends(get_async_db)) -> TrendRead:
    stmt = select(Trend).options(selectinload(Trend.sources)).filter(Trend.slug == slug)
    result = await db.execute(stmt)
    trend = result.scalars().unique().first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    return trend
