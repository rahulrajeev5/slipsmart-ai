# Principle: Repository Pattern. This keeps database queries out of routers and services.
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.modules.competitions.model import Competition
from app.modules.competitions.schema import CompetitionCreate, CompetitionUpdate


class CompetitionRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, page: int, page_size: int) -> list[Competition]:
        offset = (page - 1) * page_size

        return (
            self.db.query(Competition)
            .order_by(Competition.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

    def get_by_id(self, competition_id: uuid.UUID) -> Optional[Competition]:
        return (
            self.db.query(Competition)
            .filter(Competition.id == competition_id)
            .first()
        )

    def create(self, payload: CompetitionCreate) -> Competition:
        competition = Competition(**payload.model_dump())
        self.db.add(competition)
        self.db.commit()
        self.db.refresh(competition)
        return competition

    def update(
        self,
        competition: Competition,
        payload: CompetitionUpdate,
    ) -> Competition:
        update_data = payload.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(competition, key, value)

        self.db.commit()
        self.db.refresh(competition)
        return competition

    def delete(self, competition: Competition) -> None:
        self.db.delete(competition)
        self.db.commit()