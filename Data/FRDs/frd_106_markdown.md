# FRD-106: Send 'Account Opened' Email Notification

## 1. Functionality Summary
Once the customer's account is successfully generated and activated, the system must send an automated 'Account Opened' email to the registered email ID. This email confirms account creation, shares account details (masked), onboarding steps, and security guidelines. The system must retry sending on failure, log all email events, and ensure compliance with security standards.

## 2. Detailed Functional Description

### 2.1 Input Fields

| Field         | Type   | Mandatory | Rules                         |
|---------------|--------|-----------|-------------------------------|
| customerId    | UUID   | Yes       | Must exist in CUSTOMER table  |
| email         | String | Yes       | Must match verified email     |
| accountNumber | String | Yes       | Masked except last 4 digits   |
| accountType   | String | Yes       | SAVINGS_DIGITAL               |

### 2.2 Email Sending Flow

```
# ENDPOINT
POST /notifications/sendAccountOpenedEmail

# HEADERS
Content-Type: application/json

# REQUEST
{
  "customerId": "UUID",
  "email": "customer@mail.com",
  "accountNumber": "XXXXXX1234",
  "accountType": "SAVINGS_DIGITAL"
}

# SERVER LOGIC
1. Validate email format
2. Mask account number (XXXXXXXX1234)
3. Load HTML email template
4. Inject dynamic variables:
  customerName, maskedAccountNumber, accountType
5. Call Email Service Provider (ESP):
  POST /email/send
6. If ESP returns 5xx:
  Retry up to 3 times
7. Log event in EMAIL_AUDIT table

# RESPONSE (SUCCESS)
{
  "status": "SUCCESS",
  "message": "Email sent successfully"
}

# RESPONSE (FAILURE)
{
  "status": "FAILURE",
  "errorCode": "ERR-1064",
  "message": "Email sending failed"
}
```

### 2.3 System Behavior

**On success:**
- Email is delivered to customer
- Audit record created

**On failure:**
- Retry email sending 3 times
- If still failing → system logs ERR-1064

**On missing template:**
- Load fallback email template
- Log warning event

## 3. Error Codes

| Error Code | Description         | When Triggered            |
|------------|---------------------|---------------------------|
| ERR-1060   | Email format invalid| Regex validation fails    |
| ERR-1061   | Email not verified  | Email not confirmed in DB |
| ERR-1062   | Template missing    | HTML template not found   |
| ERR-1063   | ESP unreachable     | Timeout / 5xx             |
| ERR-1064   | Email send failure  | Retries exceeded          |
| ERR-1065   | Audit save failure  | DB insert failure         |

## 4. Preconditions
- Account number generation completed (FRD-105).
- Email ID is verified and stored in CUSTOMER table.
- Email Service Provider configuration active.

## 5. Postconditions
- Email delivered or marked as failed.
- Record created in EMAIL_AUDIT table.
- Onboarding journey marked as COMPLETE if successful.

## 6. Acceptance Criteria

| AC ID  | Acceptance Criteria                                      |
|--------|----------------------------------------------------------|
| AC-601 | System sends 'Account Opened' email upon activation.    |
| AC-602 | Masked account number appears in email.                  |
| AC-603 | Retry mechanism activates for ESP failures.              |
| AC-604 | Failures trigger ERR-1064.                               |
| AC-605 | Email audit logs must be created.                        |
| AC-606 | Fallback template loads if primary missing.              |

## 7. Data Storage Impact

**Table: EMAIL_AUDIT**
- customer_id
- email
- email_type ('ACCOUNT_OPENED')
- template_version
- send_status
- attempts
- created_at

## 8. Non-Functional Requirements
- Email send latency < 2 seconds.
- Support 200 emails/minute.
- Audit logs must be immutable.
- All emails must use TLS encryption.