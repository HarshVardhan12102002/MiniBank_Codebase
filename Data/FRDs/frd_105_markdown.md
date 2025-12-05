# FRD-105: Generate Unique Account Number

## 1. Functionality Summary
The system must generate a unique, valid account number for each new customer after KYC approval. Account numbers must follow MiniBank's defined structure, avoid collisions, and be stored in the ACCOUNT table. This account number is required for activation, transactions, and customer onboarding completion.

## 2. Detailed Functional Description

### 2.1 Account Number Structure

| Component       | Description                              |
|-----------------|------------------------------------------|
| Bank Code       | 4-digit internal bank identifier (e.g., 1023) |
| Branch Code     | 3-digit branch identifier (e.g., 001)    |
| Sequence Number | 8-digit auto-increment sequence          |

### 2.2 Generation Flow

```
# ACCOUNT NUMBER FORMAT
<bankCode><branchCode><sequence>

# EXAMPLE
1023 001 00001234

# ENDPOINT
POST /account/generate

# HEADERS
Content-Type: application/json

# REQUEST
{
  "customerId": "UUID",
  "branchCode": "001"
}

# SERVER LOGIC
1. Fetch next sequence from ACCOUNT_SEQ table
2. Construct account number:
  accountNumber = bankCode + branchCode + paddedSequence
3. Check for collisions in ACCOUNT table
4. If collision → regenerate with new sequence
5. Insert new record in ACCOUNT table:
  customer_id, account_number, status='PENDING'

# RESPONSE (SUCCESS)
{
  "status": "SUCCESS",
  "accountNumber": "102300100001234"
}

# RESPONSE (FAILURE)
{
  "status": "FAILURE",
  "errorCode": "ERR-1054",
  "message": "Account number generation failed"
}
```

### 2.3 System Behavior

**On successful generation:**
- Account number inserted into ACCOUNT table
- Returned to the caller service

**On sequence collision:**
- System retries with next sequence value

**On DB failure:**
- Throw SYSTEM ERROR and return ERR-1054

## 3. Error Codes

| Error Code | Description                  | When Triggered                |
|------------|------------------------------|-------------------------------|
| ERR-1050   | Branch code invalid          | Branch code missing/invalid   |
| ERR-1051   | Cannot fetch next sequence   | Sequence table error          |
| ERR-1052   | Account number collision     | Already exists in ACCOUNT table |
| ERR-1053   | DB insert failure            | Insert operation fails        |
| ERR-1054   | Account generation failure   | Unhandled exception           |

## 4. Preconditions
- KYC successfully approved (FRD-104).
- CUSTOMER record exists.
- ACCOUNT_SEQ table available and functional.

## 5. Postconditions
- Unique account number stored in ACCOUNT table.
- Account status set to PENDING.
- Ready for activation and Welcome Email trigger.

## 6. Acceptance Criteria

| AC ID  | Acceptance Criteria                                      |
|--------|----------------------------------------------------------|
| AC-501 | System generates unique account number as per structure. |
| AC-502 | Sequence collisions retried until resolved.              |
| AC-503 | DB insert failure triggers ERR-1053.                     |
| AC-504 | Generated account number returned to client.             |
| AC-505 | Audit logs capture generation event (masked).            |

## 7. Data Storage Impact

**Table: ACCOUNT**
- account_id (UUID)
- customer_id
- account_number
- branch_code
- status
- created_at

## 8. Non-Functional Requirements
- Account generation < 2 seconds.
- Zero collision tolerance.
- Sequence increments must be atomic.
- Supports 200 RPS.