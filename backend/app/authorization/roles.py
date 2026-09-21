from enum import Enum


class RoleName(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    STUDENT = "student"


DEFAULT_ROLES = set(RoleName)