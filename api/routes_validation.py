from fastapi import APIRouter, HTTPException
from ..schemas.customer_schema import CustomerCreate
from ..utils.validators import validate_age
from ..services.aadhaar_service import validate_aadhaar
from ..services.pan_service import validate_pan

router = APIRouter(prefix="/validate", tags=["validation"])

@router.post("/age-check")
def age_check(payload: CustomerCreate):
    if not validate_age(payload.dob):
        raise HTTPException(status_code=400, detail={"error": "RULE_AGE", "message": "You must be 18 years or older to open an account."})
    return {"status": "OK"}

@router.post("/aadhaar")
def aadhaar_validate(aadhaar: str, customerId: int | None = None):
    res = validate_aadhaar(aadhaar, customer_id=customerId)
    if res["status"] == "VALID":
        return {"status": "VALID"}
    elif res["status"] == "BLOCKED":
        raise HTTPException(status_code=429, detail=res)
    else:
        raise HTTPException(status_code=400, detail=res)

@router.post("/pan")
def pan_validate(pan: str):
    res = validate_pan(pan)
    if res["status"] == "VALID":
        return {"status": "VALID", "name": res.get("name"), "dob": res.get("dob")}
    elif res["status"] == "BLACKLISTED":
        raise HTTPException(status_code=403, detail=res)
    else:
        raise HTTPException(status_code=400, detail=res)
