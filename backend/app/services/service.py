from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError
from app.models import Service
from app.repositories.service import ServiceRepository
from app.schemas import ServiceCreate, ServiceUpdate


async def list_services(db: AsyncSession) -> list[Service]:
    return await ServiceRepository(db).get_all()


async def get_service(db: AsyncSession, service_id: int) -> Service:
    service = await ServiceRepository(db).get(service_id)
    if service is None:
        raise NotFoundError("Servicio no encontrado")
    return service


async def create_service(db: AsyncSession, data: ServiceCreate) -> Service:
    return await ServiceRepository(db).create(**data.model_dump())


async def update_service(
    db: AsyncSession, service_id: int, data: ServiceUpdate
) -> Service:
    service = await get_service(db, service_id)
    return await ServiceRepository(db).update(
        service, **data.model_dump(exclude_unset=True)
    )


async def delete_service(db: AsyncSession, service_id: int) -> None:
    service = await get_service(db, service_id)
    await ServiceRepository(db).delete(service)
