import asyncpg
from fastapi import APIRouter, HTTPException, Request
from app.models.preference import PreferenceIn, PreferenceOut

router = APIRouter()

@router.post("/preferences", response_model=PreferenceOut)
async def upsert_pref(pref: PreferenceIn, request: Request):
    pool = request.app.state.db
    try:
        await pool.execute(
            """
            INSERT INTO preferences(student_id, key, value)
            VALUES($1,$2,$3)
            ON CONFLICT (student_id, key) DO UPDATE 
              SET value = EXCLUDED.value
            """,
            pref.student_id, pref.key, pref.value
        )
        return pref
    except asyncpg.exceptions.ForeignKeyViolationError:
        # student_id did not match any students.id
        raise HTTPException(status_code=404, detail="Student not found")

@router.get("/preferences/{student_id}", response_model=list[PreferenceOut])
async def list_prefs(student_id: str, request: Request):
    pool = request.app.state.db
    rows = await pool.fetch(
        "SELECT student_id, key, value FROM preferences WHERE student_id = $1",
        student_id
    )
    return [dict(r) for r in rows]
