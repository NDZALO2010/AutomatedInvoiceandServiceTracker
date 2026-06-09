from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.invoice import Invoice, InvoiceStatus
from app.services.mailer import send_overdue_notification

scheduler = BackgroundScheduler(timezone="UTC")


def mark_overdue_and_notify() -> None:
    with SessionLocal() as db:
        now = date.today()
        invoices = db.scalars(
            select(Invoice).where(Invoice.status == InvoiceStatus.UNPAID, Invoice.due_date < now)
        ).all()
        for inv in invoices:
            inv.status = InvoiceStatus.OVERDUE
            send_overdue_notification(
                to_email=inv.client.email,
                company_name=inv.client.company_name,
                amount=str(inv.total_amount),
                invoice_id=str(inv.invoice_id),
            )
        db.commit()


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.add_job(mark_overdue_and_notify, "cron", hour=6, minute=0, id="overdue_job", replace_existing=True)
        scheduler.start()
