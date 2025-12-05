# Small stub kept in case you want to continue using KYC uploads.
import uuid
from ..config import settings
from ..database import SessionLocal

ERR_FILETYPE = "ERR-1040"
ERR_META_SAVE = "ERR-1045"

ALLOWED_MIME = {"image/png", "image/jpeg", "application/pdf"}

def validate_file(file):
    if file.content_type not in ALLOWED_MIME:
        return False, ERR_FILETYPE, "Invalid file type"
    return True, None, None

def upload_to_s3_stub(file, customer_id: int, document_type: str):
    object_key = f"kyc/{customer_id}/{document_type}/{uuid.uuid4()}.bin"
    s3_url = f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{object_key}"
    return s3_url, object_key

def save_metadata(customer_id: int, document_type: str, s3_url: str, object_key: str, mime_type: str, size: int):
    # For the small schema prototype we do not persist KYC docs table, so we return success.
    return {"status": "SUCCESS", "object_key": object_key, "s3_url": s3_url}

def handle_upload(file, customer_id: int, document_type: str):
    ok, err, msg = validate_file(file)
    if not ok:
        return {"status": "FAILURE", "error": err, "message": msg}
    s3_url, object_key = upload_to_s3_stub(file, customer_id, document_type)
    meta = save_metadata(customer_id, document_type, s3_url, object_key, file.content_type, 0)
    return meta
