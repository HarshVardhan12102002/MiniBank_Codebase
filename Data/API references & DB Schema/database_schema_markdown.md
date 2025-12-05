# MiniBank Database Schema Documentation

**Version:** 1.0.0  
**Module:** Digital Savings Account Opening  
**Author:** MiniBank Engineering

## 1. Introduction

This document provides the complete database schema for the MiniBank Digital Savings Account Opening system. The schema is designed to:

- Support regulatory-compliant onboarding
- Enforce business rules (age validation, Aadhaar/PAN validation, duplicate prevention)
- Maintain customer and account lifecycle
- Enable extensibility for future KYC/AML workflows

This version reflects the simplified schema defined in BRD/FRD v1.0 with INT-based primary keys.

## 2. Entity-Relationship Overview

The system consists of three core tables:

- **CUSTOMER** — Stores customer demographic and identity information
- **ACCOUNT** — Stores generated bank accounts linked to customers
- **AADHAAR_ATTEMPTS** — Tracks Aadhaar validation attempts for fraud control

**Relationship Summary:**

- CUSTOMER (1) → ACCOUNT (N)
- CUSTOMER (1) → AADHAAR_ATTEMPTS (0/1) (via aadhaar masking)

## 3. Database Tables

### 3.1 CUSTOMER Table

Stores personal identity data required for onboarding and KYC.

| Column      | Type        | Constraints                | Description                              |
|-------------|-------------|----------------------------|------------------------------------------|
| customer_id | INT         | PRIMARY KEY, AUTO INCREMENT| Unique customer identifier               |
| name        | VARCHAR     | NOT NULL                   | Full legal name (as per ID)              |
| dob         | DATE        | NOT NULL                   | Date of birth (age ≥ 18 required)        |
| mobile      | VARCHAR(10) | UNIQUE, NOT NULL           | Customer's mobile number                 |
| aadhaar     | VARCHAR(12) | VALID AADHAAR FORMAT       | Must pass regex: ^[0-9]{12}$             |
| pan         | VARCHAR(10) | VALID PAN FORMAT           | Must pass regex: [A-Z]{5}[0-9]{4}[A-Z]   |
| created_at  | TIMESTAMP   | DEFAULT NOW()              | Row creation timestamp                   |

**Notes**

- Aadhaar and PAN are stored at the customer level (no separate KYC table).
- Mobile uniqueness enforces Rule-05 (no duplicate accounts).

### 3.2 ACCOUNT Table

Stores bank account information created during onboarding.

| Column         | Type                            | Constraints                | Description                                   |
|----------------|---------------------------------|----------------------------|-----------------------------------------------|
| account_id     | INT                             | PRIMARY KEY, AUTO INCREMENT| Account identifier                            |
| customer_id    | INT                             | FOREIGN KEY → customer_id  | Owner of the account                          |
| account_number | VARCHAR(20)                     | UNIQUE, NOT NULL           | Bank-standard generated account number        |
| status         | ENUM('ACTIVE','PENDING_KYC')    | NOT NULL                   | Current account lifecycle status              |
| created_at     | TIMESTAMP                       | DEFAULT NOW()              | Creation timestamp                            |

**Notes**

- Account numbers follow FRD-105 generation rules.
- Status defaults to PENDING_KYC; becomes ACTIVE upon onboarding completion.

### 3.3 AADHAAR_ATTEMPTS Table

Implements Business Rule-04:
> If Aadhaar validation fails ≥3 times, block further attempts for 24 hours.

| Column            | Type        | Constraints                | Description                        |
|-------------------|-------------|----------------------------|------------------------------------|
| id                | INT         | PRIMARY KEY, AUTO INCREMENT| Attempt entry ID                   |
| customer_id       | INT         | NULLABLE                   | Linked customer (optional)         |
| aadhaar_masked    | VARCHAR(12) | INDEX                      | Masked Aadhaar (XXXXXXXX1234)      |
| attempts          | INT         | DEFAULT 0                  | Failed attempt count               |
| blocked_until     | TIMESTAMP   | NULLABLE                   | If set → Aadhaar validation blocked|
| last_attempted_at | TIMESTAMP   | DEFAULT NOW()              | Audit timestamp                    |

**Notes**

- Masked Aadhaar avoids storing raw Aadhaar, supporting data minimization.
- Used to compute retry logic per FRD-101.

## 4. Constraints & Rules Implemented at DB Level

| Rule ID | Rule Description         | Schema Enforcement                                           |
|---------|--------------------------|--------------------------------------------------------------|
| RULE-01 | Age ≥ 18                 | Enforced at application layer (DOB is stored, age computed dynamically) |
| RULE-02 | PAN regex                | Application validation before insert                         |
| RULE-03 | Aadhaar regex            | Application validation before insert                         |
| RULE-05 | Unique mobile            | UNIQUE(mobile) constraint in CUSTOMER                        |
| RULE-04 | Aadhaar fail count logic | Stored in AADHAAR_ATTEMPTS                                   |

## 5. Index Strategy

**CUSTOMER**
- `mobile` → Unique index
- `aadhaar` → Optional index if Aadhaar-based lookup needed
- `pan` → Optional index for PAN lookups

**ACCOUNT**
- `customer_id` → FK index
- `account_number` → Unique index

**AADHAAR_ATTEMPTS**
- `aadhaar_masked` → Index for fast lookup during validation

## 6. Suggested Future Extensions

### Recommended Table Additions

| Table             | Purpose                           |
|-------------------|-----------------------------------|
| kyc_documents     | Store Aadhaar/PAN image metadata  |
| email_audit       | Track email delivery status       |
| onboarding_audit  | Track onboarding step transitions |
| risk_score        | AML scoring                       |

### Potential Optimizations

- Move Aadhaar/PAN to a IDENTITY table with encryption-at-rest
- Add customer_email column (the schema currently lacks an email field)
- Switch ENUM to lookup table for multi-branch deployments

## 7. SQL DDL Scripts

### 7.1 CUSTOMER Table DDL

```sql
CREATE TABLE customer (
    customer_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR NOT NULL,
    dob             DATE NOT NULL,
    mobile          VARCHAR(10) NOT NULL UNIQUE,
    aadhaar         VARCHAR(12),
    pan             VARCHAR(10),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.2 ACCOUNT Table DDL

```sql
CREATE TABLE account (
    account_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id     INTEGER NOT NULL,
    account_number  VARCHAR(20) NOT NULL UNIQUE,
    status          TEXT CHECK(status IN ('ACTIVE','PENDING_KYC')) NOT NULL DEFAULT 'PENDING_KYC',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);
```

### 7.3 AADHAAR_ATTEMPTS Table DDL

```sql
CREATE TABLE aadhaar_attempts (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER,
    aadhaar_masked   VARCHAR(12),
    attempts         INTEGER DEFAULT 0,
    blocked_until    TIMESTAMP,
    last_attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 8. ER Diagram (Text Version)

```
   ┌─────────────┐         1 ────────── n        ┌─────────────┐
   │  CUSTOMER    │──────────────────────────────▶│   ACCOUNT    │
   └─────────────┘                                 └─────────────┘
         │
         │  optional link (via masked aadhaar)
         ▼
   ┌──────────────────┐
   │ AADHAAR_ATTEMPTS │
   └──────────────────┘
```

## 9. Summary

The updated schema is:

- Lightweight and efficient
- Aligned with BRD + FRD
- Fully suitable for MVP onboarding
- Expandable for enterprise-scale KYC systems