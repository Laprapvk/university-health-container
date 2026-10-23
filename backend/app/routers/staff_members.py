from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    StaffMemberCreate,
    StaffMemberDTO,
    StaffMemberUpdate,
)
from app.services import staff_member as staff_member_service

router = APIRouter()


@router.get("/", response_model=list[StaffMemberDTO])
async def get_staff_members(db: AsyncSession = Depends(get_db)):
    return await staff_member_service.list_staff_members(db)


@router.get("/{staff_member_id}", response_model=StaffMemberDTO)
async def get_staff_member(staff_member_id: int, db: AsyncSession = Depends(get_db)):
    return await staff_member_service.get_staff_member(db, staff_member_id)


@router.post(
    "/", response_model=StaffMemberDTO, status_code=status.HTTP_201_CREATED
)
async def create_staff_member(
    data: StaffMemberCreate, db: AsyncSession = Depends(get_db)
):
    return await staff_member_service.create_staff_member(db, data)


@router.put("/{staff_member_id}", response_model=StaffMemberDTO)
async def update_staff_member(
    staff_member_id: int,
    data: StaffMemberUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await staff_member_service.update_staff_member(db, staff_member_id, data)


@router.delete("/{staff_member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff_member(
    staff_member_id: int, db: AsyncSession = Depends(get_db)
):
    await staff_member_service.delete_staff_member(db, staff_member_id)
