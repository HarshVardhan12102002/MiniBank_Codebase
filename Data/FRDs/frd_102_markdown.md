# FRD-102: PAN Verification & Blacklist Check

## 1. Functionality Summary
The system must validate the PAN number provided by the customer. This includes format checking, blacklist validation, and mock Income Tax API verification. The PAN must be structurally correct and must not exist in the blacklist repository. Only valid PANs allow the onboarding to proceed.

## 2. Detailed Functional Description

### 2.1 Input Field

| Field      | Type             | Mandatory | Rules                                      |
|------------|------------------|-----------|-------------------------------------------|
| panNumber  | String (10 chars)| Yes       | Must match regex ^[A-Z]{5}[0-9]{4}[A-Z]{1}$ |

### 2.2 Validation Flow

```
# ENDPOINT
POST /mock-tax/validatePAN

# HEADERS
Content-Type: application/json

# REQUEST
{
  "panNumber": "ABCDE1234F"
}

# RESPONSE (VALID)
{
  "status": "VALID",
  "name": "John Doe",
  "dob": "1990-04-21"
}

# RESPONSE (INVALID)
{
  "status": "INVALID",
  "message": "PAN not found"
}

# RESPONSE (BLACKLISTED)
{
  "status": "BLACKLISTED",
  "reason": "Fraudulent activity"
}

# RESPONSE (ERROR)
{
  "status": "ERROR",
  "message": "Internal service failure"
}
```

### 2.3 System Behavior

**If status = VALID:**
- Proceed to Aadhaar/PAN cross-verification

**If status = INVALID:**
- Block onboarding and display error message

**If status = BLACKLISTED:**
- Immediately terminate onboarding
- Display generic message: 'Verification failed. Please contact support.'

**If status = ERROR:**
- Retry up to 3 times
- If still failing, mark as SYSTEM ERROR

## 3. Error Codes

| Error Code | Description            | When Triggered              |
|------------|------------------------|-----------------------------|
| ERR-1020   | PAN format invalid     | Regex validation fails      |
| ERR-1021   | PAN not found          | Mock API returns INVALID    |
| ERR-1022   | PAN blacklisted        | Mock API returns BLACKLISTED|
| ERR-1023   | Tax API unreachable    | Timeout / 5xx               |
| ERR-1024   | Malformed response     | Missing fields              |
| ERR-1025   | Too many attempts      | Retry limit exceeded        |

## 4. Preconditions
- Aadhaar validation completed successfully (FRD-101).
- PAN number input is available.
- Mock Income Tax API is reachable.

## 5. Postconditions
- PAN validation result stored in KYC table.
- Blacklist flag stored if applicable.
- If PAN is VALID → proceed to KYC document upload step.

## 6. Acceptance Criteria

| AC ID  | Acceptance Criteria                                      |
|--------|----------------------------------------------------------|
| AC-201 | System validates PAN format before API call.             |
| AC-202 | System receives VALID/INVALID/BLACKLISTED response.      |
| AC-203 | If INVALID → show 'Invalid PAN Number'.                  |
| AC-204 | If BLACKLISTED → terminate onboarding & store flag.      |
| AC-205 | API failure triggers retries before ERR-1023.            |
| AC-206 | Store PAN status and log masked request & response.      |

## 7. Data Storage Impact

**Table: KYC**

Fields updated:
- pan_number (Encrypted)
- pan_status (VALID / INVALID / BLACKLISTED)
- pan_validation_timestamp

## 8. Non-Functional Requirements
- Response time < 3 seconds.
- Mask PAN except first 3 and last 1 characters.
- Retry policy: 3 attempts with exponential backoff.
- Concurrency: ≥100 RPS.