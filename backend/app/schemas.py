from datetime import time

from pydantic import BaseModel, ConfigDict


# --- Roles ---------------------------------------------------------------
class RoleDTO(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


# --- Usuarios ------------------------------------------------------------
class UserDTO(BaseModel):
    id: int
    role_id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    role_id: int
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    role_id: int | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None


# --- Servicios -----------------------------------------------------------
class ServiceDTO(BaseModel):
    id: int
    name: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    building: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    department: str | None = None
    building: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    department: str | None = None
    building: str | None = None
    email: str | None = None
    phone: str | None = None
    website: str | None = None


# --- Personal ------------------------------------------------------------
class StaffMemberDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str | None = None
    department: str | None = None
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class StaffMemberCreate(BaseModel):
    first_name: str
    last_name: str
    position: str | None = None
    department: str | None = None
    email: str | None = None
    phone: str | None = None


class StaffMemberUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    position: str | None = None
    department: str | None = None
    email: str | None = None
    phone: str | None = None


# --- Horarios ------------------------------------------------------------
class ScheduleDTO(BaseModel):
    id: int
    service_id: int
    day_of_week: str
    opening_time: time | None = None
    closing_time: time | None = None

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(BaseModel):
    service_id: int
    day_of_week: str
    opening_time: time | None = None
    closing_time: time | None = None


class ScheduleUpdate(BaseModel):
    service_id: int | None = None
    day_of_week: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None


# --- Autenticación -------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


__all__ = [
    "RoleDTO",
    "RoleCreate",
    "RoleUpdate",
    "UserDTO",
    "UserCreate",
    "UserUpdate",
    "ServiceDTO",
    "ServiceCreate",
    "ServiceUpdate",
    "StaffMemberDTO",
    "StaffMemberCreate",
    "StaffMemberUpdate",
    "ScheduleDTO",
    "ScheduleCreate",
    "ScheduleUpdate",
    "LoginRequest",
    "Token",
]
