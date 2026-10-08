from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.authentication.security import hash_password, verify_password
from app.models import Role, User


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    # Agregamos selectinload(User.role) para cargar la relación del rol de manera asíncrona
    stmt = (
        select(User).options(selectinload(User.role)).where(User.username == username)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    user = await get_user_by_username(db, username)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


async def create_user(
    db: AsyncSession, username: str, email: str, password: str, role_id: int
) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role_id=role_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalar_one_or_none()
