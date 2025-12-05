# FRD-101: Aadhaar Validation Using UIDAI Mock API

## 1. Functionality Summary
The system must validate the Aadhaar number submitted by the customer using a UIDAI Mock API. This API simulates Aadhaar authentication responses (VALID, INVALID, ERROR). Validation ensures the Aadhaar number is structurally correct and matches UIDAI mock records before proceeding to the next onboarding step.

## 2. Detailed Functional Description

### 2.1 Input Field

| Field          | Type              | Mandatory | Rules                       |
|----------------|-------------------|-----------|----------------------------|
| aadhaarNumber  | String (12 digits)| Yes       | Must match regex ^[0-9]{12}$ |

### 2.2 Validation Flow

```
# ENDPOINT
POST /mock-uidai/validateAadhaar

# HEADERS
Content-Type: application/json

# REQUEST
{
  "aadhaarNumber": "XXXXXXXXXXXX"
}

# RESPONSE (VALID)
{
  "status": "VALID",
  "message": "Aadhaar found"
}

# RESPONSE (INVALID)
{
  "status": "INVALID",
  "message": "Not found"
}

# RESPONSE (ERROR)
{
  "status": "ERROR",
  "message": "Internal error"
}
```

### 2.3 System Behavior

**If status = VALID:**  
Proceed to FRD-102 (PAN verification).

**If status = INVALID:**  
Block onboarding and display error.

**If status = ERROR:**  
Retry API call up to 3 times. If still failing, mark as SYSTEM ERROR.

## 3. Error Codes

| Error Code | Description                  | When Triggered           |
|------------|------------------------------|--------------------------|
| ERR-1010   | Aadhaar format invalid       | Regex fails              |
| ERR-1011   | Aadhaar not found in mock DB | UIDAI returns INVALID    |
| ERR-1012   | UIDAI mock unreachable       | Timeout / 5xx            |
| ERR-1013   | Malformed response           | Missing status/message   |
| ERR-1014   | Too many attempts            | Retries exceeded         |
| ERR-1015   | Rate limit exceeded          | Mock API throttles       |

## 4. Preconditions
- Customer has already submitted personal details.
- Aadhaar number is available.
- UIDAI mock API endpoint is reachable.

## 5. Postconditions
- Aadhaar validation result stored in KYC table.
- Audit logs recorded (masked).
- If VALID → proceed to FRD-102.

## 6. Acceptance Criteria

| AC ID  | Acceptance Criteria                             |
|--------|-------------------------------------------------|
| AC-101 | System validates format before API call.        |
| AC-102 | System receives VALID/INVALID from API.         |
| AC-103 | INVALID → display 'Invalid Aadhaar Number'.     |
| AC-104 | API failure retried 3 times before ERR-1012.    |
| AC-105 | Store Aadhaar status in DB.                     |
| AC-106 | Log masked request & response.                  |

## 7. Data Storage Impact

**Table: KYC**
- aadhaar_number (Encrypted)
- aadhaar_status
- aadhaar_validation_timestamp

## 8. Non-Functional Requirements
- Response time < 3 seconds.
- Mask Aadhaar except last 4 digits in logs.
- Retry policy: 3 attempts with exponential backoff.
- Concurrency: ≥100 RPS.