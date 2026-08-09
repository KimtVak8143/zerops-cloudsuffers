import asyncio
import traceback
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.db.session import engine, AsyncSessionLocal
from app.models.trend import Trend

print('DATABASE_URL:', settings.database_url)
print('ASYNC URL:', engine.url)

async def main():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(select(1))
            print('raw SELECT 1:', result.scalar())

        async with AsyncSessionLocal() as session:
            stmt = select(Trend).options(selectinload(Trend.sources)).order_by(Trend.created_at.desc())
            result = await session.execute(stmt)
            trends = result.scalars().unique().all()
            print('trends count:', len(trends))
            for trend in trends[:3]:
                print('trend:', trend.id, trend.name, trend.category, len(trend.sources))
    except Exception as exc:
        print('ERROR:', exc)
        traceback.print_exc()

asyncio.run(main())
