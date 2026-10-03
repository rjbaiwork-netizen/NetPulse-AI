from __future__ import annotations
from alembic import op
import sqlalchemy as sa
revision="0002_customer_location"
down_revision="0001_device_geo_pop"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("customers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_code", sa.String(64), nullable=False),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("phone", sa.String(32)), sa.Column("email", sa.String(160)),
        sa.Column("address", sa.Text()), sa.Column("pppoe_username", sa.String(128)),
        sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id")),
        sa.Column("status", sa.String(16), nullable=False, server_default="active"),
        sa.Column("latitude", sa.Float()), sa.Column("longitude", sa.Float()),
        sa.Column("location_accuracy_m", sa.Float()), sa.Column("location_source", sa.String(64)),
        sa.Column("location_updated_at", sa.DateTime()), sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_index("ix_customers_customer_code","customers",["customer_code"],unique=True)
    for name,column in [("ix_customers_name","name"),("ix_customers_phone","phone"),("ix_customers_pppoe_username","pppoe_username"),("ix_customers_device_id","device_id"),("ix_customers_status","status")]:
        op.create_index(name,"customers",[column],unique=False)
    op.create_table("customer_locations",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("customer_id",sa.Integer(),sa.ForeignKey("customers.id",ondelete="CASCADE"),nullable=False),
        sa.Column("latitude",sa.Float(),nullable=False),sa.Column("longitude",sa.Float(),nullable=False),
        sa.Column("accuracy_m",sa.Float()),sa.Column("source",sa.String(64),nullable=False,server_default="gps"),
        sa.Column("captured_at",sa.DateTime(),nullable=False))
    op.create_index("ix_customer_locations_customer_id","customer_locations",["customer_id"],unique=False)
    op.create_index("ix_customer_locations_captured_at","customer_locations",["captured_at"],unique=False)
    op.create_index("ix_customer_locations_customer_captured","customer_locations",["customer_id","captured_at"],unique=False)
def downgrade():
    op.drop_index("ix_customer_locations_customer_captured",table_name="customer_locations")
    op.drop_index("ix_customer_locations_captured_at",table_name="customer_locations")
    op.drop_index("ix_customer_locations_customer_id",table_name="customer_locations")
    op.drop_table("customer_locations")
    for name in ["ix_customers_status","ix_customers_device_id","ix_customers_pppoe_username","ix_customers_phone","ix_customers_name","ix_customers_customer_code"]:
        op.drop_index(name,table_name="customers")
    op.drop_table("customers")
