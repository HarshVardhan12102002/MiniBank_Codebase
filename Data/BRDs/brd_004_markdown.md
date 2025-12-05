# BRD-004: Duplicate Mobile Number Prevention

## 1. Requirement Summary
The system must check whether the mobile number entered by the customer already exists in the MiniBank system. If the mobile number is found, onboarding must be blocked and the user must be guided to login or recover the existing account. This prevents duplicate accounts and maintains data integrity.

## 2. Detailed Description

**Mobile Number Validation Rules:**
- 10-digit Indian mobile number format
- Lookup in customer master table
- Lookup in in-progress applications
- Optional lookup in dormant/closed accounts

**When Mobile Exists:**
- Block onboarding
- Display appropriate error message
- Suggest login or account recovery

**When Mobile Does NOT Exist:**
- Proceed with onboarding
- Reserve the mobile number to prevent race conditions

Backend queries must be optimized using indexed fields. Audit logs must capture duplicate-block events.

## 3. Business Rationale
- Mobile number is a primary identifier
- Ensures regulatory compliance for unique identities
- Prevents duplicate savings accounts
- Protects against fraud and misuse
- Improves customer experience by redirecting existing users

## 4. Inputs & Outputs

| Field          | Validation                        | Mandatory |
|----------------|-----------------------------------|-----------|
| Mobile Number  | 10-digit Indian regex validation  | Yes       |

**Output:**  
Mobile status: 'Available' or 'Already Registered'. On duplicate, onboarding stops.

## 5. Acceptance Criteria

| AC ID  | Criteria                                                                      |
|--------|-------------------------------------------------------------------------------|
| AC-001 | Validate mobile number format before performing database check.               |
| AC-002 | Check customer master and in-progress applications for duplicates.            |
| AC-003 | Block onboarding if mobile exists and show correct message.                   |
| AC-004 | Allow onboarding if mobile is unique.                                         |
| AC-005 | Duplicate attempts must be logged for audit.                                  |
| AC-006 | System must prevent simultaneous onboarding using the same number.            |

## 6. Preconditions
- Customer has entered mobile number.
- Customer database available.
- Mobile field indexed for fast lookup.

## 7. Postconditions
- Unique mobile → onboarding continues.
- Duplicate → user guided to login or recovery.
- Duplicate attempt logged.

## 8. Exceptions / Edge Cases

| ID     | Scenario                          | Expected Behavior                   |
|--------|-----------------------------------|-------------------------------------|
| EC-001 | Invalid mobile number format      | Show inline error                   |
| EC-002 | Mobile exists in active customer record | Block onboarding; suggest login     |
| EC-003 | Mobile exists in incomplete applications | Prevent duplicate; suggest resume   |
| EC-004 | Database unavailable              | Show temporary error                |
| EC-005 | Rapid multiple entries            | Throttle requests                   |
| EC-006 | Simultaneous submissions          | Allow one; block the other          |