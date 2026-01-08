from fastapi import APIRouter, UploadFile, File, HTTPException
import hashlib
import os
from typing import List
from ..core.models import Case, CaseCreate
from datetime import datetime
import uuid
from ..engines.similarity.hasher import generate_video_phash


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
async def upload_evidence(case_id: str, file: UploadFile = File(...)):
    # 1 Check case exists
    if not any(case.id == case_id for case in CASES_DB):
        raise HTTPException(status_code=404, detail="Case not found")

    # 2 Read file safely (async)
    content = await file.read()

    # 3 Generate SHA256 hash
    sha256_hash = hashlib.sha256(content).hexdigest()

    # 4 Prepare storage path
    stored_filename = f"{sha256_hash}_{file.filename}"
    stored_path = os.path.join(EVIDENCE_DIR, stored_filename)

    # 5 Write file to disk FIRST
    with open(stored_path, "wb") as f:
        f.write(content)

    # 6 Generate perceptual hash AFTER file exists
    phashes = generate_video_phash(stored_path)

    # 7 Build evidence record 
    evidence_record = {
        "case_id": case_id,
        "original_filename": file.filename,
        "stored_path": stored_path,
        "sha256": sha256_hash,
        "phashes": phashes,
        "uploaded_at": datetime.utcnow().isoformat()
    }

    # 8 Store in memory
    EVIDENCE.setdefault(case_id, []).append(evidence_record)

    return evidence_record
