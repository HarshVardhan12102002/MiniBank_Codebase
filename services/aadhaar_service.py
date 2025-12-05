import requests
from ..config import settings
from ..utils.validators import validate_aadhaar_format
from ..database import SessionLocal
from ..models.aadhaar_attempt import AadhaarAttempt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

ERR_FORMAT = "ERR-1010"
ERR_NOT_FOUND = "ERR-1011"
ERR_UNREACHABLE = "ERR-1012"
ERR_MALFORMED = "ERR-1013"
ERR_TOO_MANY = "ERR-1014"

def mask_aadhaar(aadhaar: str):
    return f"XXXXXXXX{aadhaar[-4:]}"

def validate_aadhaar(aadhaar: str, customer_id: int = None):
    if not validate_aadhaar_format(aadhaar):
        return {"status": "INVALID", "error": ERR_FORMAT, "message": "Invalid Aadhaar format"}

    session: Session = SessionLocal()
    try:
        masked = mask_aadhaar(aadhaar)
        attempt = session.query(AadhaarAttempt).filter_by(aadhaar_masked=masked).first()
        if attempt and attempt.blocked_until and attempt.blocked_until > datetime.utcnow():
            return {"status": "BLOCKED", "error": ERR_TOO_MANY, "message": "Blocked due to previous failures"}

        # call UIDAI mock
        url = f"{settings.UIDAI_MOCK_URL}/validateAadhaar"
        try:
            resp = requests.post(url, json={"aadhaarNumber": aadhaar}, timeout=3)
        except requests.RequestException:
            # increment attempt
            if not attempt:
                attempt = AadhaarAttempt(customer_id=customer_id, aadhaar_masked=masked, attempts=1)
                session.add(attempt)
            else:
                attempt.attempts = (attempt.attempts or 0) + 1
                attempt.last_attempted_at = datetime.utcnow()
            session.commit()
            return {"status": "ERROR", "error": ERR_UNREACHABLE, "message": "UIDAI service unreachable"}

        if resp.status_code != 200:
            return {"status": "ERROR", "error": ERR_UNREACHABLE, "message": "UIDAI returned error"}

        data = resp.json()
        if "status" not in data:
            return {"status": "ERROR", "error": ERR_MALFORMED, "message": "Malformed UIDAI response"}

        if data["status"] == "VALID":
            # reset attempts
            if attempt:
                session.delete(attempt)
                session.commit()
            return {"status": "VALID", "message": "Aadhaar valid"}
        else:
            if not attempt:
                attempt = AadhaarAttempt(customer_id=customer_id, aadhaar_masked=masked, attempts=1, last_attempted_at=datetime.utcnow())
                session.add(attempt)
            else:
                attempt.attempts = (attempt.attempts or 0) + 1
                attempt.last_attempted_at = datetime.utcnow()

            if attempt.attempts >= 3:
                attempt.blocked_until = datetime.utcnow() + timedelta(hours=24)

            session.commit()
            return {"status": "INVALID", "error": ERR_NOT_FOUND, "message": data.get("message", "Aadhaar invalid")}
    finally:
        session.close()
