from fastapi import APIRouter
from typing import List
from ..core.models import Case, CaseCreate
from datetime import datetime
import uuid

router = APIRouter()


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
