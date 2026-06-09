import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.client import Client
from app.models.invoice import Invoice, InvoiceStatus
from app.models.user import User, UserRole
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdateStatus
from app.services.billing import calculate_client_total

router = APIRouter()


@router.post("", response_model=InvoiceRead)
def create_invoice(
    payload: InvoiceCreate,
    db: Annotated[Session, Depends(get_db)],
    _finance: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> Invoice:
    client = db.scalar(select(Client).where(Client.client_id == payload.client_id))
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    total = calculate_client_total(db, payload.client_id)
    invoice = Invoice(
        client_id=payload.client_id,
        total_amount=total,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("", response_model=list[InvoiceRead])
def list_invoices(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Invoice]:
    stmt = select(Invoice)
    if current_user.role == UserRole.CLIENT:
        if not current_user.client_id:
            return []
        stmt = stmt.where(Invoice.client_id == current_user.client_id)
    return db.scalars(stmt).all()


@router.patch("/{invoice_id}/status", response_model=InvoiceRead)
def update_invoice_status(
    invoice_id: uuid.UUID,
    payload: InvoiceUpdateStatus,
    db: Annotated[Session, Depends(get_db)],
    _finance: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> Invoice:
    invoice = db.scalar(select(Invoice).where(Invoice.invoice_id == invoice_id))
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    invoice.status = payload.status
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/overdue/preview")
def preview_overdue(
    db: Annotated[Session, Depends(get_db)],
    _finance: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> dict[str, int | str]:
    now = date.today()
    overdue_count = len(
        db.scalars(select(Invoice).where(Invoice.status == InvoiceStatus.UNPAID, Invoice.due_date < now)).all()
    )
    return {"date": now.isoformat(), "overdue_count": overdue_count}
