from app.models.invoice import InvoiceStatus
from app.tasks import scheduler


def test_tc_auto_01_overdue_transition_and_dispatch(db_session, seeded_data, monkeypatch):
    calls = []

    def fake_send_overdue_notification(to_email, company_name, amount, invoice_id):
        calls.append({
            "to_email": to_email,
            "company_name": company_name,
            "amount": amount,
            "invoice_id": invoice_id,
        })

    monkeypatch.setattr(scheduler, "send_overdue_notification", fake_send_overdue_notification)

    def fake_session_local():
        return db_session

    monkeypatch.setattr(scheduler, "SessionLocal", fake_session_local)

    scheduler.mark_overdue_and_notify()

    invoice = seeded_data["overdue_invoice"]
    db_session.refresh(invoice)
    assert invoice.status == InvoiceStatus.OVERDUE
    assert len(calls) == 1
