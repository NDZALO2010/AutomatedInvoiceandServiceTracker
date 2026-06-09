from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service


def calculate_client_total(db: Session, client_id) -> Decimal:
    services = db.scalars(select(Service).where(Service.client_id == client_id)).all()
    total = Decimal("0.00")
    for svc in services:
        total += Decimal(svc.unit_price) * Decimal(svc.quantity)
    return total.quantize(Decimal("0.01"))
