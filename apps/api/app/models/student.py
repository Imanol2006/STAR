from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StudentIn(BaseModel):
    email: str

class StudentOut(BaseModel):
    id: UUID
    email: str
    created_at: datetime
