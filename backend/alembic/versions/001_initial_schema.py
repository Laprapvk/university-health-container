"""initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-10-07

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Tabla Roles
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    # 2. Tabla Users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_role_id", "users", ["role_id"])

    # 3. Tabla Services
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("department", sa.String(length=150), nullable=True),
        sa.Column("building", sa.String(length=150), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # 4. Tabla Staff Members (si la mantienes)
    op.create_table(
        "staff_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("position", sa.String(length=150), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # 5. Tabla Schedules
    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("day_of_week", sa.String(length=20), nullable=False),
        sa.Column("opening_time", sa.Time(), nullable=True),
        sa.Column("closing_time", sa.Time(), nullable=True),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_schedules_service_id", "schedules", ["service_id"])


def downgrade() -> None:
    op.drop_index("ix_schedules_service_id", table_name="schedules")
    op.drop_table("schedules")
    op.drop_table("staff_members")
    op.drop_table("services")
    op.drop_index("ix_users_role_id", table_name="users")
    op.drop_table("users")
    op.drop_table("roles")
