from fastapi import APIRouter, HTTPException, UploadFile, File
from ..schemas.customer_schema import CustomerCreate
from ..database import SessionLocal
from ..models.customer import Customer
from ..services.onboarding_service import create_customer, full_onboarding
from ..services.kyc_service import handle_upload  # unchanged; optional in this small schema

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/create-customer")
def create_customer_route(payload: CustomerCreate):
    session = SessionLocal()
    try:
        existing = session.query(Customer).filter_by(mobile=payload.mobile).first()
        if existing:
            raise HTTPException(status_code=409, detail="Mobile number already registered")
        cust = create_customer(session, payload.dict())
        return {"status": "SUCCESS", "customer_id": cust.customer_id}
    finally:
        session.close()

@router.post("/upload-kyc/{customer_id}")
def upload_kyc(customer_id: int, aadhaarFront: UploadFile = File(None), panImage: UploadFile = File(None)):
    # Keeping the KYC upload flow but in this small schema we may only store metadata
    if aadhaarFront:
        res1 = handle_upload(aadhaarFront, customer_id, "aadhaarFront")
        if res1.get("status") != "SUCCESS":
            raise HTTPException(status_code=400, detail=res1)
    if panImage:
        res2 = handle_upload(panImage, customer_id, "panImage")
        if res2.get("status") != "SUCCESS":
            raise HTTPException(status_code=400, detail=res2)
    return {"status": "SUCCESS"}

@router.post("/onboard/{customer_id}")
def onboard_customer(customer_id: int):
    res = full_onboarding(customer_id)
    if res["status"] == "SUCCESS":
        return {"status": "SUCCESS", "accountNumber": res["accountNumber"], "emailStatus": res.get("emailStatus")}
    else:
        raise HTTPException(status_code=400, detail=res)
