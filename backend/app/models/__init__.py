from app.db.base import Base
from app.models.building import Building
from app.models.campus import Campus
from app.models.contact import Contact
from app.models.department import Department
from app.models.role import Role
from app.models.schedule import Schedule
from app.models.service import Service
from app.models.staff_member import StaffMember
from app.models.university import University
from app.models.user import User

__all__ = [
    "Base",
    "Building",
    "Campus",
    "Contact",
    "Department",
    "Role",
    "Schedule",
    "Service",
    "StaffMember",
    "University",
    "User",
]
