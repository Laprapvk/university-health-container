import enum


class RoleName(str, enum.Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    STUDENT = "STUDENT"
    GUEST = "GUEST"


DEFAULT_ROLES = [
    {"name": RoleName.ADMIN, "description": "Full administrative access"},
    {"name": RoleName.STAFF, "description": "Medical and Psychological staff"},
    {"name": RoleName.STUDENT, "description": "Student-level access"},
    {"name": RoleName.GUEST, "description": "Read-only access"},
]
