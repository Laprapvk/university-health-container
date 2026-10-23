from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictError, NotFoundError
from app.models import StaffMember
from app.repositories.staff_member import StaffMemberRepository
from app.schemas import StaffMemberCreate, StaffMemberUpdate


async def list_staff_members(db: AsyncSession) -> list[StaffMember]:
    return await StaffMemberRepository(db).get_all()


async def get_staff_member(db: AsyncSession, staff_member_id: int) -> StaffMember:
    staff_member = await StaffMemberRepository(db).get(staff_member_id)
    if staff_member is None:
        raise NotFoundError("Miembro del personal no encontrado")
    return staff_member


async def create_staff_member(
    db: AsyncSession, data: StaffMemberCreate
) -> StaffMember:
    repo = StaffMemberRepository(db)
    if data.email is not None and await repo.get_by_email(data.email) is not None:
        raise ConflictError("El correo electrónico ya está registrado")
    return await repo.create(**data.model_dump())


async def update_staff_member(
    db: AsyncSession, staff_member_id: int, data: StaffMemberUpdate
) -> StaffMember:
    repo = StaffMemberRepository(db)
    staff_member = await get_staff_member(db, staff_member_id)

    values = data.model_dump(exclude_unset=True)
    if values.get("email") is not None:
        existing = await repo.get_by_email(values["email"])
        if existing is not None and existing.id != staff_member_id:
            raise ConflictError("El correo electrónico ya está registrado")

    return await repo.update(staff_member, **values)


async def delete_staff_member(db: AsyncSession, staff_member_id: int) -> None:
    staff_member = await get_staff_member(db, staff_member_id)
    await StaffMemberRepository(db).delete(staff_member)
