# BRD-003: KYC Completion

## 1. Requirement Summary
The customer must complete full KYC verification to activate the digital savings account. This includes uploading required documents, entering additional information, and undergoing automated/manual verification. The account is activated only after successful KYC approval.

## 2. Detailed Description

### 1. Document Upload
- Aadhaar front & back
- PAN card copy
- Passport-size photograph
- Signature image

System validates file type, size, and clarity, and stores files in encrypted form.

### 2. Additional Customer Information
- Address (permanent & communication)
- Occupation
- Marital status
- Annual income range
- Nominee details (optional)

### 3. Verification Process
Automated KYC checks run first. If failed, application moves to manual review. Officer may approve, reject, or request resubmission.

### 4. Status Flow
Pending Upload → Under Review → Approved / Rejected / Resubmission Required

## 3. Business Rationale
- Compliance with RBI KYC regulations
- Prevention of fraud and identity theft
- AML/CFT compliance
- Ensures accurate customer identity before activation

## 4. Inputs & Outputs

| Field            | Validation                      | Mandatory |
|------------------|---------------------------------|-----------|
| Aadhaar Image    | Valid file type/size, clear     | Yes       |
| PAN Image        | Valid file type/size            | Yes       |
| Photograph       | Clear face image                | Yes       |
| Signature        | Readable signature              | Yes       |
| Address Details  | Valid pincode, non-empty        | Yes       |
| Occupation       | From master list                | Yes       |
| Income Range     | From category list              | Yes       |
| Nominee Details  | Optional fields                 | No        |

**Output:**  
KYC record stored with status: Approved / Rejected / Resubmission Required.

## 5. Acceptance Criteria

| AC ID  | Criteria                                                          |
|--------|-------------------------------------------------------------------|
| AC-001 | Validate allowed formats and file sizes for uploads.              |
| AC-002 | Detect unclear or blurry documents.                               |
| AC-003 | Automated KYC runs before manual review.                          |
| AC-004 | Reviewer can approve, reject, or request resubmission.            |
| AC-005 | KYC must be approved before account activation.                   |
| AC-006 | If rejected, system displays reason and allows re-upload.         |

## 6. Preconditions
- Aadhaar & PAN verification completed (BRD-002).
- Customer has required documents ready.
- OCR/face-match systems are operational.

## 7. Postconditions
- KYC stored in regulatory record.
- Status updated for account creation.
- Audit logs created.

## 8. Exceptions / Edge Cases

| ID     | Scenario                   | Expected Behavior         |
|--------|----------------------------|---------------------------|
| EC-001 | Blurry or unreadable image | System requests reupload  |
| EC-002 | Incorrect document uploaded| System blocks submission  |
| EC-003 | Automated KYC fails        | Route to manual review    |
| EC-004 | Manual review rejects      | Show reason to user       |
| EC-005 | User abandons mid-process  | Save as 'KYC Pending'     |
| EC-006 | File too large             | Show file size error      |
| EC-007 | Mandatory fields missing   | Block submission          |