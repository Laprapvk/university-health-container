from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictError, NotFoundError, ValidationError
from app.models import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.security import hash_password, verify_password


async def list_users(db: AsyncSession) -> list[User]:
    return await UserRepository(db).get_all()


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await UserRepository(db).get(user_id)
    if user is None:
        raise NotFoundError("Usuario no encontrado")
    return user


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    user = await UserRepository(db).get_by_username(username)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    repo = UserRepository(db)

    if await repo.get_by_username(data.username) is not None:
        raise ConflictError("El nombre de usuario ya está registrado")
    if await repo.get_by_email(data.email) is not None:
        raise ConflictError("El correo electrónico ya está registrado")
    if await RoleRepository(db).get(data.role_id) is None:
        raise ValidationError("El rol indicado no existe")

    return await repo.create(
        role_id=data.role_id,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> User:
    repo = UserRepository(db)
    user = await get_user(db, user_id)

    values = data.model_dump(exclude_unset=True)

    if "username" in values:
        existing = await repo.get_by_username(values["username"])
        if existing is not None and existing.id != user_id:
            raise ConflictError("El nombre de usuario ya está registrado")

    if "email" in values:
        existing = await repo.get_by_email(values["email"])
        if existing is not None and existing.id != user_id:
            raise ConflictError("El correo electrónico ya está registrado")

    if "role_id" in values:
        if await RoleRepository(db).get(values["role_id"]) is None:
            raise ValidationError("El rol indicado no existe")

    if "password" in values:
        values["password_hash"] = hash_password(values.pop("password"))

    return await repo.update(user, **values)


async def delete_user(db: AsyncSession, user_id: int) -> None:
    user = await get_user(db, user_id)
    await UserRepository(db).delete(user)
