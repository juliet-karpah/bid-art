from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from sqlalchemy import text
from contextlib import asynccontextmanager
from app.core.queue import get_pool
from app.routes import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.arq_pool = await get_pool()
    yield
    await app.state.arq_pool.aclose()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Bid Art"}

@app.get("/db-check")
async def db_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))

    return {
        "database": "connection successful",
        "result": result.scalar()
    }

@app.get("/vector-check")
async def vector_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT extversion FROM pg_extension WHERE extname='vector' "))

    return {"pg_vector": result.scalar()}

@app.post("/test-arq-job")
async def enqueue_first_job(request: Request):
    job = await request.app.state.arq_pool.enqueue_job(
        "first_job",
        "Arq test job from FastAPI"
    )

    return {
        "message": "Job queued",
        "job_id": job.job_id if job else None
    }