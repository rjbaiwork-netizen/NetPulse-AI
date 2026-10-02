from __future__ import annotations
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
revision="0001_device_geo_pop"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 bind=op.get_bind(); inspector=inspect(bind)
 if not inspector.has_table("devices"): return
 cols={c["name"] for c in inspector.get_columns("devices")}
 if "latitude" not in cols: op.add_column("devices",sa.Column("latitude",sa.Float(),nullable=True))
 if "longitude" not in cols: op.add_column("devices",sa.Column("longitude",sa.Float(),nullable=True))
 if "pop_name" not in cols:
  op.add_column("devices",sa.Column("pop_name",sa.String(length=128),nullable=True));op.create_index("ix_devices_pop_name","devices",["pop_name"],unique=False)
def downgrade():
 bind=op.get_bind(); inspector=inspect(bind)
 if not inspector.has_table("devices"): return
 cols={c["name"] for c in inspector.get_columns("devices")}
 if "pop_name" in cols:
  indexes={i["name"] for i in inspector.get_indexes("devices")}
  if "ix_devices_pop_name" in indexes: op.drop_index("ix_devices_pop_name",table_name="devices")
  op.drop_column("devices","pop_name")
 if "longitude" in cols: op.drop_column("devices","longitude")
 if "latitude" in cols: op.drop_column("devices","latitude")
