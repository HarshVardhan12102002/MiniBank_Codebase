# FRD-103: Store Personal Details in CUSTOMER Table

## 1. Functionality Summary
The system must store the customer's personal details in the CUSTOMER table after validation. This includes name, date of birth, email, and mobile number. The storage process must ensure data integrity, encryption for sensitive fields, and audit logging. This record becomes the primary identity reference for all subsequent onboarding operations.

## 2. Detailed Functional Description

### 2.1 Input Fields

| Field    | Type              | Mandatory | Rules                              |
|----------|-------------------|-----------|-----------------------------------|
| fullName | String            | Yes       | Alphabetic + spaces, min length 3 |
| dob      | Date              | Yes       | Age must be ≥ 18                  |
| email    | String            | Yes       | Valid email format                |
| mobile   | String (10 digits)| Yes       | Must match ^[0-9]{10}$            |

### 2.2 Data Persistence Flow

```
# ENDPOINT
POST /customer/create

# HEADERS
Content-Type: application/json

# REQUEST
{
  "fullName": "John Doe",
  "dob": "1994-02-14",
  "email": "john.doe@mail.com",
  "mobile": "9876543210"
}

# DB OPERATION (INSERT)
INSERT INTO CUSTOMER (
  customer_id,
  full_name,
  dob,
  email,
  mobile,
  created_at,
  updated_at
) VALUES (
  :uuid,
  :fullName,
  :dob,
  :email,
  :mobile,
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
);

# RESPONSE (SUCCESS)
{
  "status": "SUCCESS",
  "customerId": "UUID-GENERATED"
}

# RESPONSE (FAILURE)
{
  "status": "FAILURE",
  "errorCode": "ERR-1034",
  "message": "Failed to store customer details"
}
```

### 2.3 System Behavior

**On valid data:**
- Insert customer record into CUSTOMER table
- Generate customer_id (UUID)
- Return SUCCESS response with customerId

**On invalid data:**
- Reject request and return validation errors

**On DB failure:**
- Return SYSTEM ERROR and log event

## 3. Error Codes

| Error Code | Description                | When Triggered                    |
|------------|----------------------------|-----------------------------------|
| ERR-1030   | Full name format invalid   | Regex fails / contains numbers    |
| ERR-1031   | User under 18              | DOB rule fails                    |
| ERR-1032   | Email format invalid       | Regex fails                       |
| ERR-1033   | Mobile format invalid      | Regex fails                       |
| ERR-1034   | Database insert failure    | DB connectivity / constraint error|
| ERR-1035   | Duplicate mobile number    | Mobile already exists             |

## 4. Preconditions
- Personal details collected from BRD-001.
- Mobile uniqueness validated (BRD-004).
- CUSTOMER table exists and is reachable.

## 5. Postconditions
- New record inserted into CUSTOMER table.
- customer_id generated and returned to client.
- Audit log created for record creation.

## 6. Acceptance Criteria

| AC ID  | Acceptance Criteria                                       |
|--------|-----------------------------------------------------------|
| AC-301 | System stores valid personal details into CUSTOMER table.|
| AC-302 | System encrypts sensitive fields (email, mobile).        |
| AC-303 | Duplicate mobile → error ERR-1035.                        |
| AC-304 | DB insert failure triggers ERR-1034.                      |
| AC-305 | Successful insert returns customerId (UUID).              |
| AC-306 | Audit logs must capture stored fields (masked).          |

## 7. Data Storage Impact

**Table: CUSTOMER**

Fields affected:
- customer_id (NEW)
- full_name
- dob
- email (Encrypted)
- mobile (Encrypted)
- created_at
- updated_at

## 8. Non-Functional Requirements
- Insert operation < 2 seconds.
- Encryption must follow AES-256 standard.
- CUSTOMER table indexed on mobile + email.
- Must support 100 RPS during peak onboarding.