from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.queue import get_pool
from app.routes import auth
from fastapi.middleware.cors import CORSMiddleware
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.arq_pool = await get_pool()
    yield
    await app.state.arq_pool.aclose()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Bid Art"}