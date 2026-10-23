from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ServiceCreate, ServiceDTO, ServiceUpdate
from app.services import service as service_service

router = APIRouter()


@router.get("/", response_model=list[ServiceDTO])
async def get_services(db: AsyncSession = Depends(get_db)):
    return await service_service.list_services(db)


@router.get("/{service_id}", response_model=ServiceDTO)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    return await service_service.get_service(db, service_id)


@router.post("/", response_model=ServiceDTO, status_code=status.HTTP_201_CREATED)
async def create_service(data: ServiceCreate, db: AsyncSession = Depends(get_db)):
    return await service_service.create_service(db, data)


@router.put("/{service_id}", response_model=ServiceDTO)
async def update_service(
    service_id: int, data: ServiceUpdate, db: AsyncSession = Depends(get_db)
):
    return await service_service.update_service(db, service_id, data)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)):
    await service_service.delete_service(db, service_id)
