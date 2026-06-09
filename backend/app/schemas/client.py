import uuid

from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    company_name: str
    contact_person: str
    email: EmailStr
    phone: str


class ClientRead(BaseModel):
    client_id: uuid.UUID
    company_name: str
    contact_person: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True
