from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, ForeignKey("trends.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    url = Column(String(1000), nullable=False)
    source_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    trend = relationship("Trend", back_populates="sources")
