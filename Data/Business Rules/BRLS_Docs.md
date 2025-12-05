# Business Rules Document (BRD-Rules)
## MiniBank – Digital Savings Account Opening

## 1. Introduction

The Business Rules Document (BRD-Rules) outlines the mandatory rules governing the MiniBank Digital Savings Account Opening process. These rules ensure:

- Compliance with regulatory requirements
- Prevention of fraud, duplication, and identity misuse
- Consistent decision-making throughout onboarding
- Alignment between business, risk, compliance, and engineering teams

Each business rule includes:

- Rule ID
- Primary Rule Description
- Sub-Rules & Clarifications
- Logical Conditions
- Exceptions
- Trigger Events
- Compliance Mapping
- System Enforcement Notes

## 2. Business Rule Definitions

### RULE-01: Customer Must Be ≥ 18 Years Old

**Primary Rule Description**

A customer must be 18 years or older at the time of applying for a digital savings account.

**Sub-Rules & Clarifications**

**RULE-01.1: Age Calculation Method**
- Age = current_date – date_of_birth
- Leap years must be accounted for
- Time-of-day should not influence calculation

**RULE-01.2: Threshold Enforcement**
- Eligible: age ≥ 18
- Not Eligible: age < 18

**RULE-01.3: Customer Messaging**

If the age requirement fails:
> "You must be 18 years or older to open an account."

**Logical Condition**
```
IF age(customer.dob) < 18
    THEN reject onboarding
```

**Exceptions**

No exceptions allowed due to RBI regulations.

**Trigger Event**

Occurs during personal details submission (BRD-001).

**Compliance Mapping**

RBI KYC Master Direction: Requires legal majority age for account ownership.

**System Enforcement Notes**

- Perform age validation before Aadhaar/PAN steps to reduce overhead.
- Check must be synchronous and mandatory.

---

### RULE-02: PAN Must Match Standard Format

**Primary Rule Description**

The PAN must adhere to the official Government of India format:
```
[A-Z]{5}[0-9]{4}[A-Z]
```

**Sub-Rules & Clarifications**

**RULE-02.1: Case Sensitivity**
- PAN must be uppercase; auto-convert if lowercased.

**RULE-02.2: Length Constraint**
- Must be exactly 10 characters.

**RULE-02.3: Character Restrictions**
- No spaces, symbols, or punctuation.

**RULE-02.4: Checksum Character**
- Last character must be a letter (alphabetic).

**Logical Condition**
```
IF NOT matchesRegex(PAN, "[A-Z]{5}[0-9]{4}[A-Z]")
    THEN reject PAN validation
```

**Exceptions**

None—PAN formatting rules are statutory.

**Trigger Event**

During PAN validation workflow (FRD-102).

**Compliance Mapping**

Income Tax Act, 1961: Enforces standard PAN structure.

**System Enforcement Notes**

PAN regex validation must happen before calling the PAN API.

---

### RULE-03: Aadhaar Must Be 12-Digit Numeric

**Primary Rule Description**

Aadhaar entered by the customer must be exactly 12 characters long and strictly numeric.

**Sub-Rules & Clarifications**

**RULE-03.1: Length Enforcement**
- Only 12-digit Aadhaar numbers are acceptable.

**RULE-03.2: Numeric-Only Standard**

Pattern:
```
^[0-9]{12}$
```

**RULE-03.3: Formatting Restrictions**

Must not include:
- Spaces
- Dashes
- Hyphens
- Parentheses

**RULE-03.4: Leading Zeros**
- Permitted and should not be trimmed.

**Logical Condition**
```
IF NOT matchesRegex(aadhaar, "^[0-9]{12}$")
    THEN reject Aadhaar input
```

**Exceptions**

None permitted as per UIDAI standards.

**Trigger Event**

After Aadhaar is entered in validation step (FRD-101).

**Compliance Mapping**

UIDAI Aadhaar Authentication Specification

**System Enforcement Notes**

- Validate Aadhaar on both client-side and server-side.
- Log Aadhaar in masked form: XXXXXXXX1234.

---

### RULE-04: Aadhaar Validation Failure ≥ 3 → 24-Hour Block

**Primary Rule Description**

If Aadhaar validation fails three times in a row, block further Aadhaar verification attempts for 24 hours.

**Sub-Rules & Clarifications**

**RULE-04.1: What Counts as a Failure**
- API returns INVALID
- API returns ERROR (system or mock failure)

**RULE-04.2: Cool-Down Window**
- Block duration: 24 hours from last failed attempt.

**RULE-04.3: Reset Conditions**

Reset count when:
- Customer completes a successful Aadhaar validation
  or
- 24-hour cooldown passes

**RULE-04.4: Message to Customer**
> "Your Aadhaar verification attempts have exceeded the limit. Please try again after 24 hours."

**Logical Condition**
```
IF failureCount(aadhaar) >= 3
    THEN block user for 24 hours
```

**Exceptions**

Allowed only when:
- System-wide outage detected
- UIDAI mock service outage confirmed

**Trigger Event**

During repeat Aadhaar validation trials (FRD-101).

**Compliance Mapping**

Recommended anti-fraud onboarding control based on UIDAI guidelines.

**System Enforcement Notes**

- Maintain a persistent aadhaar_attempts counter.
- Block must persist across:
  - Sessions
  - Devices
  - Browser resets
- Admin override must be fully audited.

---

### RULE-05: Mobile Number Must Be Unique

**Primary Rule Description**

A mobile number must not already exist for any customer in the MiniBank systems.

**Sub-Rules & Clarifications**

**RULE-05.1: Check Across All States**

Check must search across:
- Active customers
- In-progress onboarding applications
- Dormant/closed customers
- Recently dropped/rejected applications

**RULE-05.2: Formatting Standards**
- Must be 10-digit numeric.
- If user inputs +91, strip it and validate remaining digits.

**RULE-05.3: Rejection Handling**

If duplicate:
> "Mobile number already registered with MiniBank."

**RULE-05.4: User Guidance**

On rejection, system must show:
- "Login to existing account"
- "Forgot password?"
- "Resume application?"

**Logical Condition**
```
IF mobileNumber EXISTS IN (CUSTOMER, APPLICATION)
    THEN reject onboarding
```

**Exceptions**

No exceptions allowed.

**Trigger Event**

During personal detail input (BRD-004).

**Compliance Mapping**

KYC + AML enforcement requiring unique identity contact mapping.

**System Enforcement Notes**

- Mobile column must be indexed for optimal lookup.
- Use atomic operations or row-level locks to avoid race conditions.

---

## 7. Summary Rule Table

| Rule ID  | Summary                                      |
|----------|----------------------------------------------|
| RULE-01  | Customer must be ≥ 18 years                  |
| RULE-02  | PAN must match official regex                |
| RULE-03  | Aadhaar must be numeric 12-digit             |
| RULE-04  | 3 failed Aadhaar attempts → 24-hour block    |
| RULE-05  | Mobile number must be unique                 |