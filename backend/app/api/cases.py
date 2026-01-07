from fastapi import APIRouter, UploadFile, File, HTTPException
import hashlib
import os
from typing import List
from ..core.models import Case, CaseCreate
from datetime import datetime
import uuid

router = APIRouter()

# =====================
# Case storage (in-memory)
# =====================
CASES_DB: List[Case] = []

@router.get("/", response_model=List[Case])
def list_cases():
    return CASES_DB

@router.post("/", response_model=Case)
def create_case(case: CaseCreate):
    new_case = Case(
        id=str(uuid.uuid4()),
        title=case.title,
        description=case.description,
        created_at=datetime.utcnow()
    )
    CASES_DB.append(new_case)
    return new_case

# =====================
# Evidence storage
# =====================
EVIDENCE = {}

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

EVIDENCE_DIR = os.path.join(BASE_DIR, "data", "evidence")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

@router.post("/{case_id}/evidence")
def upload_evidence(case_id: str, file: UploadFile = File(...)):
    # if case exists
    case_exists = any(case.id == case_id for case in CASES_DB)
    if not case_exists:
        raise HTTPException(status_code=404, detail="Case not found")

    content = file.file.read()

    # Generate SHA256 hash
    sha256_hash = hashlib.sha256(content).hexdigest()

    # Store file with hash based name
    stored_filename = f"{sha256_hash}_{file.filename}"
    stored_path = os.path.join(EVIDENCE_DIR, stored_filename)

    with open(stored_path, "wb") as f:
        f.write(content)

    evidence_record = {
        "case_id": case_id,
        "original_filename": file.filename,
        "stored_path": stored_path,
        "sha256": sha256_hash,
        "uploaded_at": datetime.utcnow().isoformat()
    }

    EVIDENCE.setdefault(case_id, []).append(evidence_record)
    return evidence_record
