from sqlalchemy import select

from app.models import StaffMember
from app.repositories.base import BaseRepository


class StaffMemberRepository(BaseRepository[StaffMember]):
    model = StaffMember

    async def get_by_email(self, email: str) -> StaffMember | None:
        result = await self.db.execute(
            select(StaffMember).where(StaffMember.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_department(self, department: str) -> list[StaffMember]:
        result = await self.db.execute(
            select(StaffMember).where(StaffMember.department == department)
        )
        return list(result.scalars().all())
