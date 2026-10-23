from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ScheduleCreate, ScheduleDTO, ScheduleUpdate
from app.services import schedule as schedule_service

router = APIRouter()


@router.get("/", response_model=list[ScheduleDTO])
async def get_schedules(db: AsyncSession = Depends(get_db)):
    return await schedule_service.list_schedules(db)


@router.get("/{schedule_id}", response_model=ScheduleDTO)
async def get_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    return await schedule_service.get_schedule(db, schedule_id)


@router.post("/", response_model=ScheduleDTO, status_code=status.HTTP_201_CREATED)
async def create_schedule(data: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    return await schedule_service.create_schedule(db, data)


@router.put("/{schedule_id}", response_model=ScheduleDTO)
async def update_schedule(
    schedule_id: int, data: ScheduleUpdate, db: AsyncSession = Depends(get_db)
):
    return await schedule_service.update_schedule(db, schedule_id, data)


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    await schedule_service.delete_schedule(db, schedule_id)
