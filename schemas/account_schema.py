from pydantic import BaseModel

class AccountCreateRequest(BaseModel):
    customer_id: int
    branch_code: str

class AccountResponse(BaseModel):
    account_id: int
    account_number: str
    status: str

    class Config:
        orm_mode = True
