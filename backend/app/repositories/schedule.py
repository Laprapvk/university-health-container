from sqlalchemy import select

from app.models import Schedule
from app.repositories.base import BaseRepository


class ScheduleRepository(BaseRepository[Schedule]):
    model = Schedule

    async def get_by_service(self, service_id: int) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule).where(Schedule.service_id == service_id)
        )
        return list(result.scalars().all())
