from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundError, ValidationError
from app.models import Schedule
from app.repositories.schedule import ScheduleRepository
from app.repositories.service import ServiceRepository
from app.schemas import ScheduleCreate, ScheduleUpdate


def _validate_times(opening_time: time | None, closing_time: time | None) -> None:
    if opening_time is not None and closing_time is not None:
        if opening_time >= closing_time:
            raise ValidationError(
                "La hora de apertura debe ser anterior a la hora de cierre"
            )


async def list_schedules(db: AsyncSession) -> list[Schedule]:
    return await ScheduleRepository(db).get_all()


async def get_schedule(db: AsyncSession, schedule_id: int) -> Schedule:
    schedule = await ScheduleRepository(db).get(schedule_id)
    if schedule is None:
        raise NotFoundError("Horario no encontrado")
    return schedule


async def create_schedule(db: AsyncSession, data: ScheduleCreate) -> Schedule:
    if await ServiceRepository(db).get(data.service_id) is None:
        raise ValidationError("El servicio indicado no existe")

    _validate_times(data.opening_time, data.closing_time)
    return await ScheduleRepository(db).create(**data.model_dump())


async def update_schedule(
    db: AsyncSession, schedule_id: int, data: ScheduleUpdate
) -> Schedule:
    schedule = await get_schedule(db, schedule_id)
    values = data.model_dump(exclude_unset=True)

    if "service_id" in values:
        if await ServiceRepository(db).get(values["service_id"]) is None:
            raise ValidationError("El servicio indicado no existe")

    opening_time = values.get("opening_time", schedule.opening_time)
    closing_time = values.get("closing_time", schedule.closing_time)
    _validate_times(opening_time, closing_time)

    return await ScheduleRepository(db).update(schedule, **values)


async def delete_schedule(db: AsyncSession, schedule_id: int) -> None:
    schedule = await get_schedule(db, schedule_id)
    await ScheduleRepository(db).delete(schedule)
