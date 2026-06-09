from typing import Annotated
from datetime import date, datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.invoice import Invoice, InvoiceStatus
from app.models.client import Client
from app.models.service import Service
from app.models.user import User, UserRole

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> dict:
    """Get comprehensive admin dashboard data"""
    now = date.today()
    
    # Get total counts
    total_clients = db.scalar(select(func.count()).select_from(Client))
    total_services = db.scalar(select(func.count()).select_from(Service))
    total_invoices = db.scalar(select(func.count()).select_from(Invoice))
    total_users = db.scalar(select(func.count()).select_from(User))
    
    # Get invoice metrics
    unpaid_invoices = db.scalars(
        select(Invoice).where(Invoice.status == InvoiceStatus.UNPAID)
    ).all()
    overdue_invoices = db.scalars(
        select(Invoice).where(
            Invoice.status == InvoiceStatus.UNPAID,
            Invoice.due_date < now
        )
    ).all()
    paid_invoices = db.scalars(
        select(Invoice).where(Invoice.status == InvoiceStatus.PAID)
    ).all()
    
    # Calculate totals
    total_unpaid = sum(inv.total_amount for inv in unpaid_invoices)
    total_overdue = sum(inv.total_amount for inv in overdue_invoices)
    total_paid = sum(inv.total_amount for inv in paid_invoices)
    total_revenue = total_paid
    
    # Get recent invoices
    recent_invoices = db.scalars(
        select(Invoice).order_by(Invoice.issue_date.desc()).limit(5)
    ).all()
    
    return {
        "statistics": {
            "total_clients": total_clients or 0,
            "total_services": total_services or 0,
            "total_invoices": total_invoices or 0,
            "total_users": total_users or 0,
        },
        "invoice_metrics": {
            "unpaid_count": len(unpaid_invoices),
            "overdue_count": len(overdue_invoices),
            "paid_count": len(paid_invoices),
            "unpaid_total": float(total_unpaid),
            "overdue_total": float(total_overdue),
            "paid_total": float(total_paid),
        },
        "financial_summary": {
            "total_revenue": float(total_revenue),
            "pending_revenue": float(total_unpaid),
            "overdue_revenue": float(total_overdue),
        },
        "recent_invoices": [
            {
                "invoice_id": str(inv.invoice_id),
                "client_id": str(inv.client_id),
                "total_amount": float(inv.total_amount),
                "issue_date": inv.issue_date.isoformat(),
                "due_date": inv.due_date.isoformat(),
                "status": inv.status.value,
            }
            for inv in recent_invoices
        ],
    }


@router.get("/dashboard/finance")
def finance_dashboard(
    db: Annotated[Session, Depends(get_db)],
    _finance: Annotated[User, Depends(require_roles(UserRole.ADMIN, UserRole.FINANCE))],
) -> dict:
    """Get comprehensive finance dashboard data"""
    now = date.today()
    
    # Get invoice metrics
    unpaid_invoices = db.scalars(
        select(Invoice).where(Invoice.status == InvoiceStatus.UNPAID)
    ).all()
    overdue_invoices = db.scalars(
        select(Invoice).where(
            Invoice.status == InvoiceStatus.UNPAID,
            Invoice.due_date < now
        )
    ).all()
    paid_invoices = db.scalars(
        select(Invoice).where(Invoice.status == InvoiceStatus.PAID)
    ).all()
    
    # Calculate totals
    total_unpaid = sum(inv.total_amount for inv in unpaid_invoices)
    total_overdue = sum(inv.total_amount for inv in overdue_invoices)
    total_paid = sum(inv.total_amount for inv in paid_invoices)
    total_revenue = total_paid
    
    # Get overdue invoices
    overdue_details = db.scalars(
        select(Invoice).where(
            Invoice.status == InvoiceStatus.UNPAID,
            Invoice.due_date < now
        ).order_by(Invoice.due_date)
    ).all()
    
    # Get top clients by revenue
    client_totals = {}
    for inv in db.scalars(select(Invoice).where(Invoice.status == InvoiceStatus.PAID)).all():
        if inv.client_id not in client_totals:
            client_totals[inv.client_id] = Decimal('0')
        client_totals[inv.client_id] += inv.total_amount
    
    # Get recent invoices
    recent_invoices = db.scalars(
        select(Invoice).order_by(Invoice.issue_date.desc()).limit(10)
    ).all()
    
    return {
        "summary": {
            "total_revenue": float(total_revenue),
            "pending_revenue": float(total_unpaid),
            "overdue_revenue": float(total_overdue),
            "paid_invoices": len(paid_invoices),
            "unpaid_invoices": len(unpaid_invoices),
            "overdue_invoices": len(overdue_invoices),
        },
        "overdue_invoices": [
            {
                "invoice_id": str(inv.invoice_id),
                "client_id": str(inv.client_id),
                "total_amount": float(inv.total_amount),
                "due_date": inv.due_date.isoformat(),
                "days_overdue": (now - inv.due_date).days,
                "status": inv.status.value,
            }
            for inv in overdue_details
        ],
        "recent_invoices": [
            {
                "invoice_id": str(inv.invoice_id),
                "client_id": str(inv.client_id),
                "total_amount": float(inv.total_amount),
                "issue_date": inv.issue_date.isoformat(),
                "due_date": inv.due_date.isoformat(),
                "status": inv.status.value,
            }
            for inv in recent_invoices
        ],
    }
