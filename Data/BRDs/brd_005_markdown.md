# BRD-005: Welcome Email Notification

## 1. Requirement Summary
Upon successful activation of the customer's digital savings account, the system must send an automated Welcome Email. The email will confirm account creation and provide important onboarding details such as account number (masked), banking instructions, and customer support information.

## 2. Detailed Description

**Email Trigger Conditions:**
- KYC status = Approved
- Account creation = Successful
- Account status = Active

**Mandatory Email Contents:**
- Customer Name
- Masked Account Number
- IFSC Code
- Account Type (Savings – Digital)
- Instructions for Mobile/App login
- Customer support details
- Security reminders
- Link to Terms & Conditions

**Formatting Requirements:**
- Use MiniBank HTML email template
- Responsive design
- Branded header & footer
- Avoid spam-triggering keywords

**Technical Requirements:**
- Email sent via approved SMTP/Notification service
- Log email status, timestamp, and template version
- Retry email sending up to 3 times on failure

**Security Requirements:**
- Masked account number (e.g., XXXX1234)
- No sensitive information (PAN/Aadhaar)
- Only send to verified email address from BRD-001

## 3. Business Rationale
- Confirms successful account creation
- Provides onboarding instructions
- Meets regulatory communication requirements
- Reduces customer confusion and support load
- Enhances MiniBank brand confidence

## 4. Inputs & Outputs

| Field          | Source                         | Mandatory |
|----------------|--------------------------------|-----------|
| Customer Name  | Customer Profile               | Yes       |
| Email Address  | BRD-001 (Personal Details)     | Yes       |
| Account Number | Core Banking System            | Yes       |
| IFSC Code      | Product Setup                  | Yes       |
| Account Status | Account Creation Module        | Yes       |

**Output:**  
Welcome Email sent and delivery status logged.

## 5. Acceptance Criteria

| AC ID  | Criteria                                                      |
|--------|---------------------------------------------------------------|
| AC-001 | Email is sent only after account activation.                  |
| AC-002 | Email uses approved HTML template.                            |
| AC-003 | Account number is masked in the notification.                 |
| AC-004 | Email is sent only to the verified email address.            |
| AC-005 | System retries sending up to 3 times upon failure.           |
| AC-006 | Email delivery event is logged with timestamp.               |

## 6. Preconditions
- KYC completed and approved (BRD-003).
- Account successfully created in CBS.
- Valid and verified email address exists in customer profile.
- Email service operational.

## 7. Postconditions
- Customer receives Welcome Email.
- Delivery status updated (Delivered / Failed).
- Onboarding journey marked as complete.

## 8. Exceptions / Edge Cases

| ID     | Scenario                      | Expected Behavior                  |
|--------|-------------------------------|------------------------------------|
| EC-001 | Invalid or undeliverable email| Retry 3 times → mark as failed     |
| EC-002 | Email server outage           | Queue email; retry later           |
| EC-003 | Missing email in profile      | Block sending and log error        |
| EC-004 | Customer reports missing email| Support can resend manually        |
| EC-005 | Email template missing        | Use fallback template and log      |
| EC-006 | Duplicate email triggers      | Prevent sending duplicates         |