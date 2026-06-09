from datetime import date, timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password
from app.db.base import Base
from app.main import app
from app.models.client import Client
from app.models.invoice import Invoice, InvoiceStatus
from app.models.service import Service
from app.models.user import User, UserRole

engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> None:
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session() -> Session:
    session = TestingSessionLocal()
    yield session
    session.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_data(db_session: Session):
    client_obj = Client(
        company_name="Acme Corp",
        contact_person="Taylor Smith",
        email="acct@acme.test",
        phone="123456789",
    )
    db_session.add(client_obj)
    db_session.flush()

    admin = User(username="admin", password_hash=hash_password("admin123"), role=UserRole.ADMIN)
    finance = User(username="finance", password_hash=hash_password("finance123"), role=UserRole.FINANCE)
    client_user = User(
        username="client1",
        password_hash=hash_password("client123"),
        role=UserRole.CLIENT,
        client_id=client_obj.client_id,
    )
    db_session.add_all([admin, finance, client_user])

    service = Service(
        client_id=client_obj.client_id,
        service_type="Mailbox Management",
        unit_price=Decimal("12.50"),
        quantity=18,
        renewal_date=date.today() + timedelta(days=30),
    )
    db_session.add(service)

    overdue_invoice = Invoice(
        client_id=client_obj.client_id,
        total_amount=Decimal("225.00"),
        issue_date=date.today() - timedelta(days=14),
        due_date=date.today() - timedelta(days=2),
        status=InvoiceStatus.UNPAID,
    )
    db_session.add(overdue_invoice)

    db_session.commit()
    return {
        "client": client_obj,
        "users": {"admin": admin, "finance": finance, "client": client_user},
        "overdue_invoice": overdue_invoice,
    }


@pytest.fixture
def admin_token() -> str:
    return create_access_token("admin", UserRole.ADMIN.value)
