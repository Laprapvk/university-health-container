from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.authentication.dependencies import get_current_user
from app.authorization.roles import RoleName
from app.models import User


def require_roles(*roles: RoleName) -> Callable:
    async def guard(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if roles and current_user.role.name not in {role.value for role in roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user

    return guard