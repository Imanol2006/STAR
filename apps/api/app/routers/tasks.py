import asyncpg
from fastapi import APIRouter, HTTPException, Request
from app.models.task import TaskIn, TaskOut

router = APIRouter()

@router.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskIn, request: Request):
    pool = request.app.state.db

    try:
        rec = await pool.fetchrow(
            """
            INSERT INTO tasks(student_id, description, due_date)
            VALUES($1, $2, $3)
            RETURNING *
            """,
            task.student_id,
            task.description,
            task.due_date,
        )

        if not rec:
            # this really shouldn’t happen if fetchrow returned None
            raise HTTPException(status_code=400, detail="Could not create task")

        return dict(rec)

    except asyncpg.exceptions.ForeignKeyViolationError:
        # e.g. student_id doesn't exist
        raise HTTPException(status_code=404, detail="Student not found")

    except asyncpg.exceptions.NotNullViolationError as e:
        # e.g. description or due_date was NULL when it shouldn’t be
        raise HTTPException(status_code=400, detail="Missing required field")

    except Exception:
        # fallback for any other error
        raise HTTPException(status_code=500, detail="Internal server error")




@router.get("/tasks/{student_id}", response_model=list[TaskOut])
async def list_tasks(student_id: str, request: Request):
    pool = request.app.state.db
    rows = await pool.fetch("SELECT * FROM tasks WHERE student_id = $1 ORDER BY created_at", student_id)
    return [dict(r) for r in rows]
