from ..database import SessionLocal
from ..services.aadhaar_service import validate_aadhaar
from ..services.pan_service import validate_pan
from ..utils.generator import generate_unique_account
from ..config import settings
from ..models.customer import Customer
from ..models.account import Account
from ..services.notification_service import send_email

def create_customer(session, data: dict):
    customer = Customer(
        name=data["name"],
        dob=data["dob"],
        mobile=data["mobile"],
        aadhaar=data.get("aadhaar"),
        pan=data.get("pan")
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def full_onboarding(customer_id: int):
    session = SessionLocal()
    try:
        cust = session.query(Customer).filter_by(customer_id=customer_id).first()
        if not cust:
            return {"status": "FAILED", "step": "NOT_FOUND", "detail": "Customer not found"}

        # Aadhaar validation
        aadhaar_res = validate_aadhaar(cust.aadhaar, customer_id=customer_id)
        if aadhaar_res["status"] != "VALID":
            return {"status": "FAILED", "step": "AADHAAR", "detail": aadhaar_res}

        # PAN validation
        pan_res = validate_pan(cust.pan)
        if pan_res["status"] != "VALID":
            return {"status": "FAILED", "step": "PAN", "detail": pan_res}

        # Account generation
        acc_num = generate_unique_account(session, settings.BANK_CODE, settings.BRANCH_CODE)
        account = Account(customer_id=customer_id, account_number=acc_num, status="ACTIVE")
        session.add(account)
        session.commit()
        session.refresh(account)

        # Notify
        html = f"<p>Welcome {cust.name}! Your account ending {acc_num[-4:]} is active.</p>"
        send_res = send_email(cust.mobile + "@example.com", "Account Opened - MiniBank", html)  # simple: email inferred for prototype
        return {"status": "SUCCESS", "accountNumber": acc_num, "emailStatus": send_res}
    finally:
        session.close()
