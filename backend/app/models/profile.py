from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class PPPoEProfile(Base):
 __tablename__="pppoe_profiles"; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(128),unique=True,index=True); download_bps:Mapped[int]=mapped_column(Integer); upload_bps:Mapped[int]=mapped_column(Integer); routeros_profile:Mapped[str]=mapped_column(String(128),default="default"); description:Mapped[str|None]=mapped_column(String(255),nullable=True)
