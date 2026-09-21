from collections.abc import Callable, Sequence

from fastapi import APIRouter, Depends

from app.authorization.guards import require_roles
from app.authorization.roles import RoleName

AUTH_ROLES_ATTR = "_auth_roles"


def access(*roles: RoleName) -> Callable:
    def decorator(func: Callable) -> Callable:
        setattr(func, AUTH_ROLES_ATTR, roles)
        return func

    return decorator


class AccessRouter(APIRouter):
    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        dependencies: Sequence[Depends] | None = None,
        **kwargs,
    ) -> None:
        roles = getattr(endpoint, AUTH_ROLES_ATTR, None)
        if roles:
            deps = list(dependencies) if dependencies else []
            deps.append(Depends(require_roles(*roles)))
            dependencies = deps
        return super().add_api_route(path, endpoint, dependencies=dependencies, **kwargs)