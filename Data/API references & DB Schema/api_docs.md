# MiniBank Onboarding API — Full OpenAPI Specification

**Version:** 1.0.0  
**Service:** MiniBank Digital Savings Account Opening

## 1. Overview

The MiniBank Onboarding API enables customers to digitally open a savings account by performing:

- Personal detail validation
- Aadhaar validation (UIDAI mock API)
- PAN validation (Tax API mock)
- KYC document upload
- Account number generation
- Welcome email notification
- Full onboarding orchestration

## 2. Base URL

```
https://api.minibank.example.com
```

(Use: `http://localhost:8000` in development)

## 3. Authentication

No authentication is required for onboarding endpoints (public flow).  
Future extensions may add OAuth / JWT.

## 4. Tags

- **Validation** — Aadhaar, PAN, Age checks
- **Onboarding** — Customer creation, account creation
- **KYC** — Document uploads
- **Service** — Health checks & metadata

## 5. Endpoints

### 🟦 5.1 Validation Endpoints

#### POST /validate/age-check

Validate whether customer meets minimum age (≥18).

**Request**
```json
{
  "fullName": "John Doe",
  "dob": "1990-05-12",
  "email": "john@mail.com",
  "mobile": "9876543210"
}
```

**Responses**

✔ **200 OK**
```json
{ "status": "OK" }
```

❌ **400 BAD REQUEST**
```json
{
  "error": "RULE_AGE",
  "message": "You must be 18 years or older to open an account."
}
```

---

#### POST /validate/aadhaar

Validates Aadhaar format + UIDAI mock API response.

**Query Parameters**

| Name       | Type   | Required |
|------------|--------|----------|
| aadhaar    | string | ✔        |
| customerId | string | optional |

**Responses**

✔ **200 VALID**
```json
{ "status": "VALID" }
```

❌ **400 INVALID**
```json
{
  "status": "INVALID",
  "error": "ERR-1011",
  "message": "Aadhaar invalid"
}
```

❌ **429 BLOCKED** (Rule-04 triggered)
```json
{
  "status": "BLOCKED",
  "error": "ERR-1014",
  "message": "Blocked due to previous failures"
}
```

---

#### POST /validate/pan

Validates PAN format + TAX mock API response.

**Query Parameters**

| Name | Type   | Required |
|------|--------|----------|
| pan  | string | ✔        |

**Responses**

✔ **200 VALID**
```json
{
  "status": "VALID",
  "name": "JOHN DOE",
  "dob": "1990-05-12"
}
```

❌ **403 BLACKLISTED**
```json
{
  "status": "BLACKLISTED",
  "error": "ERR-1022",
  "message": "Blacklisted PAN holder"
}
```

❌ **400 INVALID**
```json
{
  "status": "INVALID",
  "error": "ERR-1020",
  "message": "PAN format invalid"
}
```

---

### 🟩 5.2 Customer & Account Endpoints

#### POST /account/create-customer

Creates a new customer record.

**Request**
```json
{
  "fullName": "John Doe",
  "dob": "1994-01-20",
  "email": "john@mail.com",
  "mobile": "9876543210"
}
```

**Responses**

✔ **201 CREATED**
```json
{
  "status": "SUCCESS",
  "customerId": "eab3e830-25dd-4af1-A99a-0fd6bd2f77ea"
}
```

❌ **409 CONFLICT**
```json
{ "detail": "Mobile number already registered" }
```

---

#### POST /account/upload-kyc/{customerId}

Uploads Aadhaar/PAN documents.

**Form Data**

| Field        | Type | Required |
|--------------|------|----------|
| aadhaarFront | file | ✔        |
| panImage     | file | ✔        |

**Responses**

✔ **200**
```json
{ "status": "SUCCESS" }
```

❌ **400**
```json
{
  "status": "FAILURE",
  "error": "ERR-1040",
  "message": "Invalid file type"
}
```

---

#### POST /account/onboard/{customerId}

Full onboarding:
- Aadhaar validation
- PAN validation
- KYC doc verification
- Account number creation
- Welcome email

**Request**

Query params:
- `aadhaar=123412341234`
- `pan=ABCDE1234F`

**Responses**

✔ **200 SUCCESS**
```json
{
  "status": "SUCCESS",
  "accountNumber": "102300100001234"
}
```

❌ **400 FAILURES**

Examples:
- Aadhaar failure
- PAN mismatch
- Account generation failure
- Email failure

```json
{
  "status": "FAILED",
  "step": "AADHAAR",
  "detail": { "error": "ERR-1011" }
}
```

---

### 🟧 5.3 Service Endpoints

#### GET /

Returns service metadata.

```json
{
  "service": "MiniBank Onboarding",
  "version": "1.0.0",
  "status": "UP"
}
```

---

#### GET /health

Heartbeat.

```json
{ "health": "OK" }
```

---

#### GET /meta/service-info

```json
{
  "service": "MiniBank Onboarding",
  "modules": [
    "ValidationEngine",
    "KYC",
    "Onboarding",
    "AccountNumberEngine",
    "NotificationEngine"
  ],
  "bankCode": "1023",
  "branchCode": "001"
}
```

---

## 6. Error Code Reference

### Aadhaar Errors (FRD-101)

| Code     | Meaning                          |
|----------|----------------------------------|
| ERR-1010 | Invalid Aadhaar format           |
| ERR-1011 | Aadhaar not found                |
| ERR-1012 | UIDAI unreachable                |
| ERR-1013 | UIDAI malformed response         |
| ERR-1014 | Too many attempts (24h block)    |
| ERR-1015 | UIDAI rate limit                 |

### PAN Errors (FRD-102)

| Code     | Meaning                     |
|----------|-----------------------------|
| ERR-1020 | PAN invalid format          |
| ERR-1021 | PAN not found               |
| ERR-1022 | PAN blacklisted             |
| ERR-1023 | PAN service unreachable     |
| ERR-1024 | PAN malformed response      |

### KYC Errors (FRD-104)

| Code     | Meaning                |
|----------|------------------------|
| ERR-1040 | Invalid file type      |
| ERR-1041 | File too large         |
| ERR-1042 | Unreadable image       |
| ERR-1043 | S3 unreachable         |
| ERR-1044 | Upload failed          |
| ERR-1045 | Metadata save error    |

### Email Notification Errors (FRD-106)

| Code     | Meaning              |
|----------|----------------------|
| ERR-1060 | Invalid email        |
| ERR-1061 | Email not verified   |
| ERR-1062 | Template missing     |
| ERR-1063 | ESP unreachable      |
| ERR-1064 | Email failure        |
| ERR-1065 | Audit log failure    |

---

⭐ **End of OpenAPI MD Document**