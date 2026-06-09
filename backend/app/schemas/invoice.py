import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models.invoice import InvoiceStatus


class InvoiceCreate(BaseModel):
    client_id: uuid.UUID
    issue_date: date
    due_date: date


class InvoiceUpdateStatus(BaseModel):
    status: InvoiceStatus


class InvoiceRead(BaseModel):
    invoice_id: uuid.UUID
    client_id: uuid.UUID
    total_amount: Decimal
    issue_date: date
    due_date: date
    status: InvoiceStatus

    class Config:
        from_attributes = True
