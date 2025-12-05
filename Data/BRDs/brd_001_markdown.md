# BRD-001: Capture Personal Details

## 1. Requirement Summary
Customers must provide their basic personal information as the first step in the digital savings account opening journey. This data is essential to establish identity, validate eligibility, and initiate Aadhaar/PAN verification.

## 2. Detailed Description
The system must present a form to the customer where the following mandatory details are collected:
- Full Name
- Date of Birth
- Email Address
- Mobile Number

The system must ensure that:
- All fields are validated for correct format and completeness.
- Mobile number and email follow standard regex validation.
- Date of birth falls within permissible age limits for opening a bank account (e.g., ≥18 years).
- Name is captured exactly as per official identity documents.

These personal details become part of the initial customer record, which is used in subsequent verification and KYC steps.

## 3. Business Rationale
Accurate personal information is required to:
- Pre-validate Aadhaar and PAN identity (downstream processes)
- Ensure regulatory compliance with KYC norms
- Establish a communication channel through email/SMS
- Avoid erroneous or fraudulent onboarding attempts

Without correct personal details, the onboarding cannot proceed.

## 4. Inputs & Outputs

| Field          | Validation                                           | Mandatory |
|----------------|------------------------------------------------------|-----------|
| Full Name      | Alphabetic + spaces; min length; no special characters | Yes       |
| Date of Birth  | Valid date, age ≥ 18                                 | Yes       |
| Email          | Valid email format                                   | Yes       |
| Mobile Number  | 10-digit Indian mobile regex                         | Yes       |

**Output:**  
A customer record saved in the system with status: "Personal Details Completed"

## 5. Acceptance Criteria

| AC ID  | Criteria                                                                                      |
|--------|-----------------------------------------------------------------------------------------------|
| AC-001 | System must reject incomplete forms with clear field-level error messages.                    |
| AC-002 | System must validate mobile and email format before allowing submission.                      |
| AC-003 | System must prevent DOB that indicates customer is below minimum age.                         |
| AC-004 | On valid submission, customer record must be created and moved to the next step in onboarding flow. |

## 6. Preconditions
- Customer has initiated the digital account opening flow.
- Customer has access to the mobile device and internet.

## 7. Postconditions
- Customer's basic profile is stored in the database.
- System is ready to perform Aadhaar/PAN verification (BRD-002).

## 8. Exceptions / Edge Cases

| ID     | Scenario                          | Expected Behavior                                   |
|--------|-----------------------------------|-----------------------------------------------------|
| EC-001 | Invalid email or mobile format    | System shows inline error & blocks submission       |
| EC-002 | DOB indicates age < 18            | System rejects and displays "Not eligible for account" |
| EC-003 | Name contains invalid characters  | Show "Enter name as per official ID"                |