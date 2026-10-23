from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get(self, entity_id: int) -> User | None:
        return await self.db.get(User, entity_id, options=[selectinload(User.role)])

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User).options(selectinload(User.role)))
        return list(result.scalars().all())

    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.role))
            .where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).options(selectinload(User.role)).where(User.email == email)
        )
        return result.scalar_one_or_none()
