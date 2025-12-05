# BRD-002: Aadhaar & PAN Verification

## 1. Requirement Summary
The system must validate the customer's Aadhaar and PAN details before allowing the creation of a savings account. These identity checks ensure compliance with regulatory requirements, prevent fraud, and allow downstream KYC and account creation processes to proceed securely.

## 2. Detailed Description

**Aadhaar Verification:**
- Validate 12-digit Aadhaar number format.
- Trigger UIDAI OTP-based authentication.
- Receive verification result: success / fail / mismatch.

**PAN Verification:**
- Validate PAN format (AAAAA9999A).
- Validate PAN using Income Tax / CKYC service.
- Cross-check PAN name and DOB with personal details.
- Receive status: Valid / Invalid / Name mismatch / DOB mismatch.

Aadhaar and PAN must both pass verification before onboarding can progress. Any mismatch or failure must halt the process.

## 3. Business Rationale
- Ensure compliance with statutory KYC and AML regulations.
- Prevent identity fraud and duplicate account creation.
- Ensure accurate mapping of customer identity across systems.
- Enable seamless account activation without manual intervention.

## 4. Inputs & Outputs

| Field          | Validation                                        | Mandatory |
|----------------|---------------------------------------------------|-----------|
| Aadhaar Number | 12-digit numeric, UIDAI verification, OTP         | Yes       |
| PAN Number     | AAAAA9999A format, PAN database validation        | Yes       |

**Outputs:**  
Verified Aadhaar & PAN status saved. Status marked as "Identity Verification Completed".

## 5. Acceptance Criteria

| AC ID  | Criteria                                                                  |
|--------|---------------------------------------------------------------------------|
| AC-001 | System must validate Aadhaar format and reject invalid entries.           |
| AC-002 | System must perform UIDAI OTP-based Aadhaar authentication.               |
| AC-003 | System must validate PAN format before calling verification API.          |
| AC-004 | PAN name & DOB must match user-provided details.                          |
| AC-005 | If Aadhaar or PAN verification fails, onboarding must stop.               |
| AC-006 | On successful verification, system moves to KYC stage.                    |

## 6. Preconditions
- Customer has completed BRD-001 (Personal Details).
- UIDAI & PAN verification services are available.
- Customer has access to Aadhaar-linked mobile number.

## 7. Postconditions
- Aadhaar & PAN statuses stored.
- System ready for KYC document upload (BRD-003).
- Audit logs created for verification steps.

## 8. Exceptions / Edge Cases

| ID     | Scenario                        | Expected Behavior                              |
|--------|---------------------------------|------------------------------------------------|
| EC-001 | Invalid Aadhaar number          | Reject input and show inline error             |
| EC-002 | UIDAI OTP fails                 | Allow retry; block after 3 failures            |
| EC-003 | PAN format invalid              | Show immediate format error                    |
| EC-004 | PAN name mismatch               | Show "Details do not match PAN records"        |
| EC-005 | PAN DOB mismatch                | Prompt re-entry or correction                  |
| EC-006 | Verification API unavailable    | Display maintenance message                    |
| EC-007 | User tries to skip verification | Block progression                              |