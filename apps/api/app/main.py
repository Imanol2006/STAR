from fastapi import FastAPI
from app.db.session import get_pool
from app.routers import api_router

app = FastAPI(title="STAR API")

@app.on_event("startup")
async def startup():
    #create and store the database pool
    app.state.db = await get_pool()

app.include_router(api_router, prefix="/api")
