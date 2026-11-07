from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from sqlalchemy import text

app = FastAPI()

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