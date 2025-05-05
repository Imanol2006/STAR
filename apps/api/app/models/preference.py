from pydantic import BaseModel
from uuid import UUID

class PreferenceIn(BaseModel):
    student_id: UUID
    key: str
    value: str

class PreferenceOut(PreferenceIn):
    pass
