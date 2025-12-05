import re
from datetime import date

PAN_REGEX = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
AADHAAR_REGEX = re.compile(r'^[0-9]{12}$')

def validate_pan_format(pan: str) -> bool:
    if pan is None:
        return False
    return bool(PAN_REGEX.match(pan.upper()))

def validate_aadhaar_format(aadhaar: str) -> bool:
    if not aadhaar:
        return False
    return bool(AADHAAR_REGEX.match(aadhaar))

def calculate_age(dob: date) -> int:
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def validate_age(dob: date, min_age: int = 18) -> bool:
    return calculate_age(dob) >= min_age
