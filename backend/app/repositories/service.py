from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Service
from app.repositories.base import BaseRepository


class ServiceRepository(BaseRepository[Service]):
    model = Service

    async def get(self, entity_id: int) -> Service | None:
        return await self.db.get(
            Service, entity_id, options=[selectinload(Service.schedules)]
        )

    async def get_all(self) -> list[Service]:
        result = await self.db.execute(
            select(Service).options(selectinload(Service.schedules))
        )
        return list(result.scalars().all())
