from datetime import datetime
from pydantic import BaseModel, Field
from app.models.customer import CustomerStatus
class CustomerBase(BaseModel):
    customer_code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=160)
    phone: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=160)
    address: str | None = None
    pppoe_username: str | None = Field(default=None, max_length=128)
    device_id: int | None = None
    status: CustomerStatus = CustomerStatus.ACTIVE
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    location_accuracy_m: float | None = Field(default=None, ge=0)
    location_source: str | None = Field(default=None, max_length=64)
    notes: str | None = None
class CustomerCreate(CustomerBase):
    pass
class CustomerUpdate(BaseModel):
    customer_code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    phone: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=160)
    address: str | None = None
    pppoe_username: str | None = Field(default=None, max_length=128)
    device_id: int | None = None
    status: CustomerStatus | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    location_accuracy_m: float | None = Field(default=None, ge=0)
    location_source: str | None = Field(default=None, max_length=64)
    notes: str | None = None
class CustomerRead(CustomerBase):
    id: int
    location_updated_at: datetime | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
class CustomerLocationCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accuracy_m: float | None = Field(default=None, ge=0)
    source: str = Field(default="gps", min_length=1, max_length=64)
    captured_at: datetime | None = None
class CustomerLocationRead(CustomerLocationCreate):
    id: int
    customer_id: int
    captured_at: datetime
    model_config = {"from_attributes": True}
