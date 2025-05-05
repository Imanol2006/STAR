from fastapi import APIRouter, HTTPException, Request
import asyncpg
from app.models.student import StudentIn, StudentOut
from typing import List 
router = APIRouter()

@router.post("/profile", response_model=StudentOut)
async def create_profile(data: StudentIn, request: Request):
    pool = request.app.state.db
    try:
        rec = await pool.fetchrow(
            "INSERT INTO students(email) VALUES($1) RETURNING *",
            data.email
        )
        # return inside the try so UniqueViolationError is caught below
        return dict(rec)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Email already registered")


@router.get("/profile/{student_id}", response_model=StudentOut)
async def get_profile(student_id: str, request: Request):
    pool = request.app.state.db
    row = await pool.fetchrow("SELECT * FROM students WHERE id = $1", student_id)
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return dict(row)

@router.get("/profile", response_model=List[StudentOut])
async def list_profiles(request: Request):
    rows = await request.app.state.db.fetch("SELECT * FROM students")
    return [dict(r) for r in rows]
