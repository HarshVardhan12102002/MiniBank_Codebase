from ..config import settings
from ..database import SessionLocal
from ..models.account import Account
from sqlalchemy import select
import threading

lock = threading.Lock()

def format_account_number(bank_code: str, branch_code: str, sequence: int) -> str:
    seq_str = str(sequence).zfill(8)
    return f"{bank_code}{branch_code}{seq_str}"

def get_next_sequence(session):
    # read last sequence by account_number's last 8 digits
    rows = session.execute(select(Account.account_number)).scalars().all()
    if not rows:
        return settings.SEQUENCE_START
    sequences = []
    for acc in rows:
        try:
            sequences.append(int(str(acc)[-8:]))
        except Exception:
            continue
    if not sequences:
        return settings.SEQUENCE_START
    return max(sequences) + 1

def generate_unique_account(session, bank_code: str, branch_code: str):
    with lock:
        for _ in range(5):
            seq = get_next_sequence(session)
            acc_num = format_account_number(bank_code, branch_code, seq)
            exists = session.query(Account).filter_by(account_number=acc_num).first()
            if not exists:
                return acc_num
        raise Exception("ERR-1054: Account generation failed")
