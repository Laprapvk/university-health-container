from fastapi import Depends, HTTPException, status

from app.authentication.dependencies import (
    get_current_user,  # Ajusta la importación a tu función de usuario actual
)
from app.authorization.roles import RoleName
from app.models.user import User


class RoleGuard:
    """Clase para validar que el usuario tenga uno de los roles permitidos."""

    def __init__(self, allowed_roles: list[RoleName]):
        self.allowed_roles = [
            r.value if isinstance(r, RoleName) else r for r in allowed_roles
        ]

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role_name.upper()
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {', '.join(self.allowed_roles)}",
            )
        return current_user


# --- Accesos preconfigurados para tus rutas ---
require_admin = RoleGuard([RoleName.ADMIN])
require_staff_or_admin = RoleGuard([RoleName.ADMIN, RoleName.STAFF])
require_student_or_above = RoleGuard([RoleName.ADMIN, RoleName.STAFF, RoleName.STUDENT])
