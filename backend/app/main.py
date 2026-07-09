from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import SessionLocal
from app.modules.competitions.router import router as competitions_router

app = FastAPI(
    title="SlipSmart AI API",
    description="Backend API for SlipSmart AI",
    version="1.0.0",
)

app.include_router(competitions_router)


@app.get("/")
def root():
    return {"message": "Welcome to SlipSmart AI 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    finally:
        db.close()