import smtplib
from email.mime.text import MIMEText
from ..config import settings
from ..database import SessionLocal
from ..models.aadhaar_attempt import AadhaarAttempt  # used only for import placeholder

ERR_ESP = "ERR-1063"

def send_email(customer_email: str, subject: str, html_body: str):
    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = "no-reply@minibank.example"
    msg["To"] = customer_email

    try:
        s = smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT, timeout=5)
        s.sendmail(msg["From"], [customer_email], msg.as_string())
        s.quit()
    except Exception as ex:
        return {"status": "FAILURE", "error": ERR_ESP, "message": str(ex)}
    return {"status": "SUCCESS"}
