# Principle: API schemas are separate from database models. This prevents exposing database internals directly.
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompetitionBase(BaseModel):
    name: str
    country: Optional[str] = None
    sport: str
    season: Optional[str] = None


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    sport: Optional[str] = None
    season: Optional[str] = None


class CompetitionResponse(CompetitionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True