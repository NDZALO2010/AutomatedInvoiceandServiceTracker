from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import select

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Client, User, UserRole


DEMO_ACCOUNTS = (
    {"username": "admin", "password": "admin123", "role": UserRole.ADMIN},
    {"username": "finance", "password": "finance123", "role": UserRole.FINANCE},
    {"username": "client1", "password": "client123", "role": UserRole.CLIENT},
)


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)


def get_or_create_client(session) -> Client:
    client = session.scalar(select(Client).where(Client.company_name == "Acme Corp"))
    if client:
        return client

    client = Client(
        company_name="Acme Corp",
        contact_person="Taylor Smith",
        email="acct@acme.test",
        phone="123456789",
    )
    session.add(client)
    session.flush()
    return client


def get_or_create_user(session, username: str, password: str, role: UserRole, client_id=None) -> User:
    user = session.scalar(select(User).where(User.username == username))
    if user:
        return user

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
        client_id=client_id,
    )
    session.add(user)
    return user


def main() -> None:
    ensure_schema()
    with SessionLocal() as session:
        client = get_or_create_client(session)
        get_or_create_user(session, "admin", "admin123", UserRole.ADMIN)
        get_or_create_user(session, "finance", "finance123", UserRole.FINANCE)
        get_or_create_user(session, "client1", "client123", UserRole.CLIENT, client.client_id)
        session.commit()

    print("Seed complete.")
    print("Demo login accounts:")
    print("- admin / admin123")
    print("- finance / finance123")
    print("- client1 / client123")


if __name__ == "__main__":
    main()