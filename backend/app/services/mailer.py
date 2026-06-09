import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_overdue_notification(to_email: str, company_name: str, amount: str, invoice_id: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Overdue Invoice Notice - {company_name}"
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg.set_content(
        "\n".join(
            [
                f"Hello {company_name},",
                "",
                "An invoice is now overdue.",
                f"Invoice ID: {invoice_id}",
                f"Amount Due: {amount}",
                "Please settle the balance at your earliest convenience.",
            ]
        )
    )

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        if settings.smtp_username:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(msg)
