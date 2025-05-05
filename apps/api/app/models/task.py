from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime

class TaskIn(BaseModel):
    student_id: UUID
    description: str
    due_date: date | None

class TaskOut(TaskIn):
    id: UUID
    created_at: datetime
