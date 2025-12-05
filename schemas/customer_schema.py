from pydantic import BaseModel, constr
from datetime import date

class CustomerCreate(BaseModel):
    name: constr(min_length=3)
    dob: date
    mobile: constr(regex=r'^[0-9]{10}$')
    aadhaar: constr(regex=r'^[0-9]{12}$')
    pan: constr(regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$')

class CustomerResponse(BaseModel):
    customer_id: int
    name: str
    dob: date
    mobile: str
    aadhaar: str | None
    pan: str | None

    class Config:
        orm_mode = True
