import requests
from ..config import settings
from ..utils.validators import validate_pan_format

ERR_FORMAT = "ERR-1020"
ERR_NOT_FOUND = "ERR-1021"
ERR_BLACKLISTED = "ERR-1022"
ERR_UNREACHABLE = "ERR-1023"
ERR_MALFORMED = "ERR-1024"

def validate_pan(pan: str):
    if not pan:
        return {"status": "INVALID", "error": ERR_FORMAT, "message": "PAN missing"}
    pan_up = pan.upper()
    if not validate_pan_format(pan_up):
        return {"status": "INVALID", "error": ERR_FORMAT, "message": "PAN format invalid"}

    url = f"{settings.PAN_MOCK_URL}/validatePAN"
    try:
        resp = requests.post(url, json={"panNumber": pan_up}, timeout=3)
    except requests.RequestException:
        return {"status": "ERROR", "error": ERR_UNREACHABLE, "message": "PAN service unreachable"}

    if resp.status_code != 200:
        return {"status": "ERROR", "error": ERR_UNREACHABLE, "message": "PAN service returned error"}

    data = resp.json()
    if "status" not in data:
        return {"status": "ERROR", "error": ERR_MALFORMED, "message": "Malformed PAN response"}

    if data["status"] == "VALID":
        return {"status": "VALID", "name": data.get("name"), "dob": data.get("dob")}
    elif data["status"] == "BLACKLISTED":
        return {"status": "BLACKLISTED", "error": ERR_BLACKLISTED, "message": data.get("reason", "Blacklisted")}
    else:
        return {"status": "INVALID", "error": ERR_NOT_FOUND, "message": data.get("message", "PAN invalid")}
