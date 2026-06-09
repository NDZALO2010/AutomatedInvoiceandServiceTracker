import uuid
from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.client import Client
from app.models.invoice import Invoice, InvoiceStatus
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.client import ClientCreate, ClientRead

router = APIRouter()


@router.post("", response_model=ClientRead)
def create_client(
    payload: ClientCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> Client:
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("", response_model=list[ClientRead])
def list_clients(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> list[Client]:
    return db.scalars(select(Client)).all()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(
    client_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Client:
    client = db.scalar(select(Client).where(Client.client_id == client_id))
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    if current_user.role == UserRole.CLIENT and current_user.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Client scope violation")
    return client


@router.get("/{client_id}/dashboard")
def client_dashboard(
    client_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Get client dashboard data for personal invoice and service overview"""
    # Verify client exists
    client = db.scalar(select(Client).where(Client.client_id == client_id))
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    
    # Check access permissions
    if current_user.role == UserRole.CLIENT and current_user.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Client scope violation")
    
    now = date.today()
    
    # Get client's invoices
    invoices = db.scalars(
        select(Invoice).where(Invoice.client_id == client_id)
    ).all()
    
    # Get client's services
    services = db.scalars(
        select(Service).where(Service.client_id == client_id)
    ).all()
    
    # Calculate metrics
    paid_invoices = [inv for inv in invoices if inv.status == InvoiceStatus.PAID]
    unpaid_invoices = [inv for inv in invoices if inv.status == InvoiceStatus.UNPAID]
    overdue_invoices = [
        inv for inv in unpaid_invoices if inv.due_date < now
    ]
    
    total_paid = sum(inv.total_amount for inv in paid_invoices)
    total_unpaid = sum(inv.total_amount for inv in unpaid_invoices)
    total_overdue = sum(inv.total_amount for inv in overdue_invoices)
    
    return {
        "client_info": {
            "client_id": str(client.client_id),
            "company_name": client.company_name,
            "contact_person": client.contact_person,
            "email": client.email,
            "phone": client.phone,
        },
        "invoice_summary": {
            "total_invoices": len(invoices),
            "paid_invoices": len(paid_invoices),
            "unpaid_invoices": len(unpaid_invoices),
            "overdue_invoices": len(overdue_invoices),
            "total_paid": float(total_paid),
            "total_unpaid": float(total_unpaid),
            "total_overdue": float(total_overdue),
        },
        "active_services": len([s for s in services if s.active]),
        "total_services": len(services),
        "invoices": [
            {
                "invoice_id": str(inv.invoice_id),
                "total_amount": float(inv.total_amount),
                "issue_date": inv.issue_date.isoformat(),
                "due_date": inv.due_date.isoformat(),
                "status": inv.status.value,
                "days_until_due": (inv.due_date - now).days,
            }
            for inv in sorted(invoices, key=lambda x: x.due_date, reverse=True)
        ],
        "services": [
            {
                "service_id": str(s.service_id),
                "service_name": s.service_name,
                "description": s.description,
                "hourly_rate": float(s.hourly_rate),
                "active": s.active,
            }
            for s in services
        ],
    }
