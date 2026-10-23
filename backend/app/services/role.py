from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictError, NotFoundError
from app.models import Role
from app.repositories.role import RoleRepository
from app.schemas import RoleCreate, RoleUpdate


async def list_roles(db: AsyncSession) -> list[Role]:
    return await RoleRepository(db).get_all()


async def get_role(db: AsyncSession, role_id: int) -> Role:
    role = await RoleRepository(db).get(role_id)
    if role is None:
        raise NotFoundError("Rol no encontrado")
    return role


async def create_role(db: AsyncSession, data: RoleCreate) -> Role:
    repo = RoleRepository(db)
    if await repo.get_by_name(data.name) is not None:
        raise ConflictError(f"El rol '{data.name}' ya existe")
    return await repo.create(**data.model_dump())


async def update_role(db: AsyncSession, role_id: int, data: RoleUpdate) -> Role:
    repo = RoleRepository(db)
    role = await get_role(db, role_id)

    values = data.model_dump(exclude_unset=True)
    if "name" in values:
        existing = await repo.get_by_name(values["name"])
        if existing is not None and existing.id != role_id:
            raise ConflictError(f"El rol '{values['name']}' ya existe")

    return await repo.update(role, **values)


async def delete_role(db: AsyncSession, role_id: int) -> None:
    repo = RoleRepository(db)
    role = await get_role(db, role_id)

    if await repo.has_users(role_id):
        raise ConflictError("No se puede eliminar un rol con usuarios asignados")

    await repo.delete(role)
