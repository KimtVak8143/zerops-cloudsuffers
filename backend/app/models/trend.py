from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    slug = Column(String(220), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
    tldr = Column(Text, nullable=True)
    why_it_matters = Column(Text, nullable=True)
    momentum = Column(String(50), nullable=True)
    tech_stack = Column(JSONB, nullable=True)
    related_trends = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    sources = relationship("Source", back_populates="trend", cascade="all, delete-orphan")
