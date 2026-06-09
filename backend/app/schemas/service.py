import uuid
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, conint


class ServiceCreate(BaseModel):
    client_id: uuid.UUID
    service_type: str
    unit_price: Decimal
    quantity: conint(ge=0)
    renewal_date: date


class ServiceRead(BaseModel):
    service_id: uuid.UUID
    client_id: uuid.UUID
    service_type: str
    unit_price: Decimal
    quantity: int
    renewal_date: date

    class Config:
        from_attributes = True
