from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.service import ServiceCreate, ServiceRead

router = APIRouter()


@router.post("", response_model=ServiceRead)
def create_service(
    payload: ServiceCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> Service:
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.get("", response_model=list[ServiceRead])
def list_services(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> list[Service]:
    return db.scalars(select(Service)).all()
