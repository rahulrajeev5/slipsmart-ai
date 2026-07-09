# Principle: Single Responsibility Principle (SRP)

# Each layer has one responsibility:
# Client
#    │
#    ▼
# Router       → HTTP (requests, responses, status codes)
#    │
#    ▼
# Service      → Business logic
#    │
#    ▼
# Repository   → Database queries
#    │
#    ▼
# PostgreSQL
import uuid

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.competitions.repository import CompetitionRepository
from app.modules.competitions.schema import (
    CompetitionCreate,
    CompetitionResponse,
    CompetitionUpdate,
)
from app.modules.competitions.service import CompetitionService

router = APIRouter(prefix="/competitions", tags=["Competitions"])


def get_service(db: Session = Depends(get_db)) -> CompetitionService:
    repository = CompetitionRepository(db)
    return CompetitionService(repository)


@router.get("", response_model=list[CompetitionResponse])
def list_competitions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: CompetitionService = Depends(get_service),
):
    return service.list_competitions(page=page, page_size=page_size)


@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(
    competition_id: uuid.UUID,
    service: CompetitionService = Depends(get_service),
):
    return service.get_competition(competition_id)


@router.post(
    "",
    response_model=CompetitionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_competition(
    payload: CompetitionCreate,
    service: CompetitionService = Depends(get_service),
):
    return service.create_competition(payload)


@router.put("/{competition_id}", response_model=CompetitionResponse)
def update_competition(
    competition_id: uuid.UUID,
    payload: CompetitionUpdate,
    service: CompetitionService = Depends(get_service), #Dependency Injection principle
):
    return service.update_competition(competition_id, payload)


@router.delete("/{competition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_competition(
    competition_id: uuid.UUID,
    service: CompetitionService = Depends(get_service),
):
    service.delete_competition(competition_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)