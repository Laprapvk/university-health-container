import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


async def get_health(db: AsyncSession) -> dict:
    try:
        await asyncio.wait_for(db.execute(text("SELECT 1")), timeout=2.0)
        db_status = "connected"
    except Exception:
        db_status = "error"
    return {"status": "ok", "database": db_status}


@router.get("")
@router.get("/")
async def check_health(db: AsyncSession = Depends(get_db)):
    return await get_health(db)
