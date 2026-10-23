from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RoleCreate, RoleDTO, RoleUpdate
from app.services import role as role_service

router = APIRouter()


@router.get("/", response_model=list[RoleDTO])
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await role_service.list_roles(db)


@router.get("/{role_id}", response_model=RoleDTO)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    return await role_service.get_role(db, role_id)


@router.post("/", response_model=RoleDTO, status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await role_service.create_role(db, data)


@router.put("/{role_id}", response_model=RoleDTO)
async def update_role(
    role_id: int, data: RoleUpdate, db: AsyncSession = Depends(get_db)
):
    return await role_service.update_role(db, role_id, data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    await role_service.delete_role(db, role_id)
