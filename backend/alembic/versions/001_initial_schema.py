"""Create initial University Health schema."""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001_initial_schema"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "universities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("website", sa.String(255)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
    )
    op.create_index("ix_universities_name", "universities", ["name"], unique=True)

    op.create_table(
        "campuses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("university_id", sa.Integer(), sa.ForeignKey("universities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("address", sa.String(255), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("postal_code", sa.String(20)),
        sa.Column("phone", sa.String(30)),
    )
    op.create_index("ix_campuses_university_id", "campuses", ["university_id"])
    op.create_index("ix_campuses_name", "campuses", ["name"])

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("campus_id", sa.Integer(), sa.ForeignKey("campuses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(30)),
        sa.Column("address", sa.String(255)),
        sa.Column("description", sa.Text()),
    )
    op.create_index("ix_buildings_campus_id", "buildings", ["campus_id"])
    op.create_index("ix_buildings_name", "buildings", ["name"])
    op.create_index("ix_buildings_code", "buildings", ["code"])

    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("campus_id", sa.Integer(), sa.ForeignKey("campuses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("code", sa.String(30)),
        sa.Column("description", sa.Text()),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
    )
    op.create_index("ix_departments_campus_id", "departments", ["campus_id"])
    op.create_index("ix_departments_name", "departments", ["name"])
    op.create_index("ix_departments_code", "departments", ["code"])

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Text()),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("buildings.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("category", sa.String(100)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
        sa.Column("website", sa.String(255)),
    )
    op.create_index("ix_services_department_id", "services", ["department_id"])
    op.create_index("ix_services_building_id", "services", ["building_id"])
    op.create_index("ix_services_name", "services", ["name"])
    op.create_index("ix_services_category", "services", ["category"])

    op.create_table(
        "staff_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("position", sa.String(150)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
    )
    op.create_index("ix_staff_members_department_id", "staff_members", ["department_id"])
    op.create_index("ix_staff_members_last_name", "staff_members", ["last_name"])

    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service_id", sa.Integer(), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("value", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
    )
    op.create_index("ix_contacts_service_id", "contacts", ["service_id"])

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service_id", sa.Integer(), sa.ForeignKey("services.id", ondelete="CASCADE"), nullable=False),
        sa.Column("day_of_week", sa.String(20), nullable=False),
        sa.Column("opening_time", sa.Time()),
        sa.Column("closing_time", sa.Time()),
    )
    op.create_index("ix_schedules_service_id", "schedules", ["service_id"])

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
    )
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("schedules")
    op.drop_table("contacts")
    op.drop_table("staff_members")
    op.drop_table("services")
    op.drop_table("roles")
    op.drop_table("departments")
    op.drop_table("buildings")
    op.drop_table("campuses")
    op.drop_table("universities")
