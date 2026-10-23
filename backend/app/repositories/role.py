from sqlalchemy import func, select

from app.models import Role, User
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    model = Role

    async def get_by_name(self, name: str) -> Role | None:
        result = await self.db.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    async def has_users(self, role_id: int) -> bool:
        result = await self.db.execute(
            select(func.count()).select_from(User).where(User.role_id == role_id)
        )
        return result.scalar_one() > 0
