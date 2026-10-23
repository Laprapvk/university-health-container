from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Operaciones CRUD comunes para cualquier modelo SQLAlchemy."""

    model: type[ModelT]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, entity_id: int) -> ModelT | None:
        return await self.db.get(self.model, entity_id)

    async def get_all(self) -> list[ModelT]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, **values: Any) -> ModelT:
        entity = self.model(**values)
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def update(self, entity: ModelT, **values: Any) -> ModelT:
        for field, value in values.items():
            setattr(entity, field, value)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self.db.delete(entity)
        await self.db.commit()
