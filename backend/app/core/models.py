from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Case(BaseModel):
    id: str
    title: str
    description: Optional[str]=None
    created_at: datetime
