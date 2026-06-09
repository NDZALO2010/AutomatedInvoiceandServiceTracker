import uuid

from pydantic import BaseModel

from app.models.user import UserRole


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole
    client_id: uuid.UUID | None = None


class UserRead(BaseModel):
    user_id: uuid.UUID
    username: str
    role: UserRole
    client_id: uuid.UUID | None = None

    class Config:
        from_attributes = True
