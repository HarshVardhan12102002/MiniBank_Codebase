# MiniBank - Digital Savings Account Opening (Updated Schema)

This repo contains a FastAPI backend prototype updated to the small DB schema:
- CUSTOMER table uses integer PK (customer_id)
- CUSTOMER stores name, dob, mobile, aadhaar, pan
- ACCOUNT table uses integer PK and FK -> customer_id

## Quickstart
1. Create venv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
