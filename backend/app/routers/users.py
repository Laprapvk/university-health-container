from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import UserCreate, UserDTO, UserUpdate
from app.services import user as user_service

router = APIRouter()


@router.get("/", response_model=list[UserDTO])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_service.list_users(db)


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.get_user(db, user_id)


@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create_user(db, data)


@router.put("/{user_id}", response_model=UserDTO)
async def update_user(
    user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    return await user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    await user_service.delete_user(db, user_id)
