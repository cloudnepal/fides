"""system_dictionary_migration

Revision ID: 39397820a0d5
Revises: 3a47ce736a37
Create Date: 2023-08-03 20:07:46.326248

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "39397820a0d5"
down_revision = "3a47ce736a37"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("ctl_systems", sa.Column("vendor_id", sa.String(), nullable=True))
    op.add_column(
        "ctl_systems",
        sa.Column(
            "dataset_references",
            sa.ARRAY(sa.String()),
            server_default="{}",
            nullable=False,
        ),
    )
    op.add_column(
        "ctl_systems",
        sa.Column(
            "processes_personal_data", sa.BOOLEAN(), server_default="t", nullable=False
        ),
    )
    op.add_column(
        "ctl_systems",
        sa.Column(
            "exempt_from_privacy_regulations",
            sa.BOOLEAN(),
            server_default="f",
            nullable=False,
        ),
    )
    op.add_column(
        "ctl_systems", sa.Column("reason_for_exemption", sa.String(), nullable=True)
    )
    op.add_column(
        "ctl_systems",
        sa.Column("uses_profiling", sa.BOOLEAN(), server_default="f", nullable=False),
    )
    op.add_column(
        "ctl_systems",
        sa.Column("legal_basis_for_profiling", sa.String(), nullable=True),
    )
    op.add_column(
        "ctl_systems",
        sa.Column(
            "does_international_transfers",
            sa.BOOLEAN(),
            server_default="f",
            nullable=False,
        ),
    )
    op.add_column(
        "ctl_systems",
        sa.Column("legal_basis_for_transfers", sa.String(), nullable=True),
    )
    op.add_column(
        "ctl_systems",
        sa.Column(
            "requires_data_protection_assessments",
            sa.BOOLEAN(),
            server_default="f",
            nullable=False,
        ),
    )
    op.add_column("ctl_systems", sa.Column("dpa_location", sa.String(), nullable=True))
    op.add_column("ctl_systems", sa.Column("dpa_progress", sa.String(), nullable=True))

    op.add_column(
        "ctl_systems", sa.Column("privacy_policy", sa.String(), nullable=True)
    )
    op.add_column("ctl_systems", sa.Column("legal_name", sa.String(), nullable=True))
    op.add_column("ctl_systems", sa.Column("legal_address", sa.String(), nullable=True))
    op.add_column(
        "ctl_systems",
        sa.Column(
            "responsibility", sa.ARRAY(sa.String()), server_default="{}", nullable=True
        ),
    )
    op.add_column("ctl_systems", sa.Column("dpo", sa.String(), nullable=True))
    op.add_column(
        "ctl_systems", sa.Column("joint_controller_info", sa.String(), nullable=True)
    )
    op.add_column(
        "ctl_systems", sa.Column("data_security_practices", sa.String(), nullable=True)
    )
    op.add_column(
        "privacydeclaration",
        sa.Column(
            "features", sa.ARRAY(sa.String()), server_default="{}", nullable=False
        ),
    )
    op.add_column(
        "privacydeclaration",
        sa.Column("legal_basis_for_processing", sa.String(), nullable=True),
    )
    op.add_column(
        "privacydeclaration",
        sa.Column("impact_assessment_location", sa.String(), nullable=True),
    )
    op.add_column(
        "privacydeclaration", sa.Column("retention_period", sa.String(), nullable=True)
    )
    op.add_column(
        "privacydeclaration",
        sa.Column(
            "processes_special_category_data",
            sa.BOOLEAN(),
            server_default="f",
            nullable=False,
        ),
    )
    op.add_column(
        "privacydeclaration",
        sa.Column("special_category_legal_basis", sa.String(), nullable=True),
    )
    op.add_column(
        "privacydeclaration",
        sa.Column(
            "data_shared_with_third_parties",
            sa.BOOLEAN(),
            server_default="f",
            nullable=False,
        ),
    )
    op.add_column(
        "privacydeclaration", sa.Column("third_parties", sa.String(), nullable=True)
    )
    op.add_column(
        "privacydeclaration",
        sa.Column(
            "shared_categories",
            sa.ARRAY(sa.String()),
            server_default="{}",
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("privacydeclaration", "shared_categories")
    op.drop_column("privacydeclaration", "third_parties")
    op.drop_column("privacydeclaration", "data_shared_with_third_parties")
    op.drop_column("privacydeclaration", "special_category_legal_basis")
    op.drop_column("privacydeclaration", "processes_special_category_data")
    op.drop_column("privacydeclaration", "retention_period")
    op.drop_column("privacydeclaration", "impact_assessment_location")
    op.drop_column("privacydeclaration", "legal_basis_for_processing")
    op.drop_column("privacydeclaration", "features")
    op.drop_column("ctl_systems", "data_security_practices")
    op.drop_column("ctl_systems", "joint_controller_info")
    op.drop_column("ctl_systems", "dpo")
    op.drop_column("ctl_systems", "responsibility")
    op.drop_column("ctl_systems", "legal_address")
    op.drop_column("ctl_systems", "legal_name")
    op.drop_column("ctl_systems", "privacy_policy")
    op.drop_column("ctl_systems", "dpa_progress")
    op.drop_column("ctl_systems", "dpa_location")
    op.drop_column("ctl_systems", "requires_data_protection_assessments")
    op.drop_column("ctl_systems", "legal_basis_for_transfers")
    op.drop_column("ctl_systems", "does_international_transfers")
    op.drop_column("ctl_systems", "legal_basis_for_profiling")
    op.drop_column("ctl_systems", "uses_profiling")
    op.drop_column("ctl_systems", "reason_for_exemption")
    op.drop_column("ctl_systems", "exempt_from_privacy_regulations")
    op.drop_column("ctl_systems", "processes_personal_data")
    op.drop_column("ctl_systems", "dataset_references")
    op.drop_column("ctl_systems", "vendor_id")
    # ### end Alembic commands ###
